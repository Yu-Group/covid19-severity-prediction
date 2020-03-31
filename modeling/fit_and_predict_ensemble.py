import sklearn
import copy
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
# from viz import viz
from bokeh.plotting import figure, show, output_notebook, output_file, save
from functions import merge_data
from sklearn.model_selection import RandomizedSearchCV
import load_data
import naive_autoreg_baselines
import exponential_modeling
import pmdl_weight
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import fit_and_predict

very_important_vars = ['PopulationDensityperSqMile2010',
#                        'MedicareEnrollment,AgedTot2017',
                       'PopulationEstimate2018',
                       '#ICU_beds',
                       'MedianAge2010',
                       'Smokers_Percentage',
                       'DiabetesPercentage',
                       'HeartDiseaseMortality',
                        '#Hospitals']

exponential = {'model_type':'exponential'}
shared_exponential = {'model_type':'shared_exponential'}
demographics = {'model_type':'shared_exponential', 'demographic_vars':very_important_vars}


def fit_and_predict_ensemble(df, 
                             target_day,
                             outcome='deaths', 
                             methods=[],
                             mode='predict_future', 
                             output_key=None):
    
    """
    Function for ensemble prediction
    Input:
        df: pd.DataFrame
        target_day: array
        outcome: str 
        method: list of dictionary
            each dictionary specify the type and parameters of the model
        mode: str
        output_key: str
    Output:
        df with ensemble prediction
    """
    
    predictions = {}
    for (i, model) in enumerate(methods):
        
        if 'demographic_vars' in model:
            demographic_vars = model['demographic_vars']
        else:
            demographic_vars = []
            
        predictions[i] = fit_and_predict.fit_and_predict(df, 
                                         outcome=outcome, 
                                         method=model['model_type'], 
                                         mode=mode, 
                                         target_day=target_day,
                                         output_key=f'y_preds_{i}',
                                         demographic_vars=demographic_vars)[f'y_preds_{i}'].values
            
    if mode == 'predict_future':
        use_df = df
    else:
        use_df = exponential_modeling.leave_t_day_out(df, target_day[-1])
            
    
    weights = pmdl_weight.compute_pmdl_weight(use_df, 
                                              methods=methods, 
                                              outcome=outcome)
    sum_weights = np.zeros(len(use_df))
    for model_index in weights:
        sum_weights = sum_weights + np.array(weights[model_index])
    
    #weighted_preds = np.zeros((len(use_df), len(target_day)))
    weighted_preds = [np.zeros(len(target_day)) for i in range(len(use_df))]
    for i in range(len(df)):
        for model_index in weights:
            weighted_preds[i] += np.array(predictions[model_index][i]) * weights[model_index][i] / sum_weights[i]
        
        
    df[output_key] = weighted_preds
    return df
            
        
    
    
    
    
    
    
    
    

