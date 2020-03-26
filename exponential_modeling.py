import sklearn
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from viz import viz
from bokeh.plotting import figure, show, output_notebook, output_file, save
from functions import merge_data
from sklearn.model_selection import RandomizedSearchCV
import load_data
import copy
import statsmodels.api as sm

def exponential_fit(counts):
    
    predicted_counts = []
    for i in range(len(counts)):
        ts = counts[i]
        if ts[-1] > 100:
            start = np.where(ts >= 10)[0][0]
        elif ts[-1] >= 1:
            start = np.where(ts >= 1)[0][0]
        else:
            start = len(ts)
        active_day = len(ts) - start
        if active_day >= 3 and ts[-1] > 5:
            predictors = np.transpose(np.vstack((np.array(range(active_day)), 
                                      np.ones(active_day))))
            m = sm.GLM(ts[start:], predictors,
                       family=sm.families.Poisson())
            m = m.fit()
            predicted_counts.append(int(m.predict([active_day, 1])[0]))
        else:
            predicted_counts.append(ts[-1])  
                
    return predicted_counts 




def estimate_cases(df, method="exponential"):
    
    predicted_cases = []
    
    if method == "exponential":
        predicted_cases = exponential_fit(df['cases'].values)
    
    df['predicted_cases'] = predicted_cases
    return df
                
    
def estimate_death_rate(df, method="constant"):
    
    predicted_death_rate = []
    
    if method == 'constant':
        for i in range(len(df)):
            predicted_death_rate.append(df['deaths'].values[i][-1]/max(1, df['cases'].values[i][-1]))
            
    df['predicted_death_rate'] = predicted_death_rate
    return df
    
    
def estimate_deaths(df, method="exponential"):
    
    predicted_deaths = []
    
    if method == 'exponential':
        predicted_deaths = np.array(exponential_fit(df['deaths'].values))
        
    elif method == 'cases_exponential_rate_constant':
        predicted_cases = np.array(estimate_cases(df, method="exponential")['predicted_cases'])
        predicted_death_rate = np.array(estimate_death_rate(df, method="constant")['predicted_death_rate'])
        predicted_deaths = predicted_cases * predicted_death_rate
        
    df[f'predicted_deaths_{method}'] = predicted_deaths.astype(int)
        
    return df
        
def create_leave_one_day_out_valid(df):
    
    df2 = copy.deepcopy(df)
    days = len(df['deaths'].values[0])
    for i in range(len(df)):
        df2['deaths'].values[i] = df2['deaths'].values[i][0:(days-1)]
        df2['cases'].values[i] = df2['cases'].values[i][0:(days-1)]
    return df2

