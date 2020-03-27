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


def fit_and_predict(train_df, test_df, method, target_day=np.array([1])):
    """
    Trains a method (method) to predict a current number of days ahead (target_day)
    Predicts the values of the number of deaths for the final day of test_df and writes to the column
    'predicted_deaths_'+method+'_'+str(target_day[-1]) of the test_df
    
    Input:
    train_df, tests: dfs with county level deaths and cases
    method: string
    target_day = np.array([1,2,..,n]) predicts these number of days ahead (can just be np.array([3])) for example)

    Output:
    test_df 
    """
        
    if method == 'AR':
        print('currently deprecated')
        raise NotImplementedError
        loss, model, best_window = naive_autoreg_baselines.train_and_evaluate_model(train_df,test_df)
        return naive_autoreg_baselines.make_predictions(test_df,model,best_window)
    
    elif method == 'exponential':
        train_df = exponential_modeling.estimate_deaths(train_df, target_day=target_day)
        test_df['predicted_deaths_'+method+'_'+str(target_day[-1])] = train_df['predicted_deaths_exponential']
        return test_df
    
    elif method == 'shared_exponential':
        if target_day != np.array([1]):
            raise NotImplementedError
        # Fit a poisson GLM with shared parameters across counties. Input to the poisson GLM is log(previous_days_deaths+1)
        cur_day_predictions = exponential_modeling.fit_and_predict_shared_exponential(train_df,test_df)
        test_df['predicted_deaths_'+method+'_'+str(target_day[-1])] = cur_day_predictions
        return test_df
    else:
        print('Unknown method')
        raise ValueError