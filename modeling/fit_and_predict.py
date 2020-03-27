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

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor


def fit_and_predict(train_df, test_df, method, mode, target_day=np.array([1])):
    """
    Trains a method (method) to predict a current number of days ahead (target_day)
    Predicts the values of the number of deaths for the final day of test_df and writes to the column
    'predicted_deaths_'+method+'_'+str(target_day[-1]) of the test_df
    
    Input:
    train_df, tests: dfs with county level deaths and cases
    method: string
    target_day = np.array([1,2,..,n]) predicts these number of days ahead (can just be np.array([3])) for example if you just want 3 days ahead)
    mode: either 'predict_future' or 'eval_mode'
    predict_future is predicting deaths on FUTURE days, so target_day=np.array([1])) means it predicts tomorrow's deaths
    eval_mode is for evaluating the performance of the classifier. target_day=np.array([k])) will predict the current days death count
    using information from k days ago. target_day= np.array([1,2,3,...,k]) will predict todays deaths, yesterdays deaths, deaths k-1 days ago
    using information from k days ago.


    Output:
    test_df 
    """
        
    assert mode == 'predict_future' or mode == 'eval_mode', 'unknown mode'
    if method == 'AR':
        print('currently deprecated')
        raise NotImplementedError
        loss, model, best_window = naive_autoreg_baselines.train_and_evaluate_model(train_df,test_df)
        return naive_autoreg_baselines.make_predictions(test_df,model,best_window)
    
    elif method == 'exponential':
        test_df = exponential_modeling.estimate_deaths(test_df, mode, target_day=target_day)
        test_df['predicted_deaths_'+method+'_'+str(target_day[-1])] = test_df['predicted_deaths_exponential']
        del test_df['predicted_deaths_exponential']

        return test_df
    
    elif method == 'shared_exponential':
        if target_day != np.array([1]):
            raise NotImplementedError
        # Fit a poisson GLM with shared parameters across counties. Input to the poisson GLM is log(previous_days_deaths+1)
        cur_day_predictions = exponential_modeling.fit_and_predict_shared_exponential(train_df,test_df,mode)
        test_df['predicted_deaths_'+method+'_'+str(target_day[-1])] = cur_day_predictions
        return test_df
    else:
        print('Unknown method')
        raise ValueError
        

def get_forecasts(df,
                  outcome,
                  method, 
                  target_day=np.array([1]),
                  output_key):
    
    """
    This is a tentative interface for extracting cases/deaths forecasts of future days
    
    df: county_level df
    outcome: 'cases' or 'deaths'
    method: currently only support 'exponential' and 'shared_exponential'
    target_day:
    output_key
    
    output: df with forecasts in output_key 
    """
    
    
    if method == 'exponential':
        return exponential_modeling.get_exponential_forecasts(df=df, 
                                                              outcome=outcome, 
                                                              target_day=target_day,
                                                              output_key=output_key)
         
    
    elif method == 'shared_exponential':
        if target_day != np.array([1]):
            raise NotImplementedError
        ###
        
    
    else:
        print('Unknown method')
        raise ValueError        
