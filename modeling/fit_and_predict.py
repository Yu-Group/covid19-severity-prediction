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
    
    if method == 'AR':
        loss, model, best_window = naive_autoreg_baselines.train_and_evaluate_model(train_df,test_df)
        return naive_autoreg_baselines.make_predictions(test_df,model,best_window)
    
    elif method == 'exponential':
        train_df = exponential_modeling.estimate_deaths(train_df, target_day=target_day)
        test_df['predicted_deaths_exponential'] = train_df['predicted_deaths_exponential']
        return test_df
    
    else:
        print('Unknown method')
        raise ValueError