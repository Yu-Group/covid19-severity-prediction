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
import fit_and_predict

def pmdl_weight(y, y_preds):
    
    """
    function to compute the pmdl weights.
    y: observed outcome
    y_preds: predicted outcome
    y and y_preds must have the same shape
    
    Output: 
    """
    
    assert y.shape == y_preds.shape, 'y and y_preds have different shapes'
    
    n, t = y.shape
    c0, mu = 2, 0.9
    
    error_weights = c0 * (1-mu) * np.array([mu**i for i in range(t-1, -1, -1)])
    model_weights = []
    for i in range(n):
        error = np.abs(np.array(y_preds[i]) - np.array(y[i]))
        model_weights.append(np.exp(-np.sum(error * error_weights)))
        
    return np.array(model_weights)

def compute_pmdl_weight(df, methods, outcome):
    
    y = np.array([df[outcome].values[i][-7:] for i in range(len(df))])
    weights = {}
    for method in methods:
        
        y_preds = np.zeros(y.shape)
        for t in range(1, 8):
            
            df2 = exponential_modeling.leave_t_day_out(df, t)
            df2 = fit_and_predict.get_forecasts(df2,
                                outcome=outcome,
                                method=method,
                                output_key='y_preds',
                                target_day=np.array([1]))
            y_preds[:,(7-t)] = np.array([df2['y_preds'].values[i][0] for i in range(len(df))])
            
        weights[method] = pmdl_weight(y, y_preds)
        
    return weights
    

        
        
        
        
        
        
    