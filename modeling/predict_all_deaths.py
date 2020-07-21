#!/usr/bin/python3

import sys
sys.path.append('../') 
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
#from functions import merge_data
from sklearn.model_selection import RandomizedSearchCV
#import load_data
#import data_new
from datetime import datetime, timedelta, date

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

import fit_and_predict
import warnings
warnings.filterwarnings("ignore")
from models import exponential_modeling
from pmdl_weight import pmdl_weight

from tqdm import tqdm

very_important_vars = ['PopulationDensityperSqMile2010',
#                        'MedicareEnrollment,AgedTot2017',
                       'PopulationEstimate2018',
                       '#ICU_beds',
                       'MedianAge2010',
                       'Smokers_Percentage',
                       'DiabetesPercentage',
                       'HeartDiseaseMortality',
                       #'Respiratory Mortality',
                        '#Hospitals']
methods = ['advanced_shared_model', 'linear', 'shared_exponential', 
           'demographic', 'exponential']
advanced_model = {'model_type':'advanced_shared_model'}
linear = {'model_type':'linear'}
corrected = False
df_county = pd.read_pickle("df_county_6_21.pkl")
today = date(2020, 6, 21) 
earliest_day = date(2020, 3, 7) 
ndays = (today - earliest_day).days
outcome = 'deaths'
horizon = 21

if corrected:
    """
    correcting the uptick on 4/14
    """
    df_county_orig = load_data.load_county_level(data_dir = '../data/')
    df_county_predictions = pd.read_pickle("all_deaths_preds_6_21.pkl")
    df_county = copy.deepcopy(df_county_orig)
    #today = date(2020, 6, 8)
    uptick_date = date(2020, 4, 14)
    days_to_correct = (today - uptick_date).days
    for i in range(len(df_county)):
        r = df_county.iloc[i]
        if r['StateName'] == 'NY':
            pred = df_county_predictions[f'all_deaths_pred_4_14_ensemble_21'].values[i][0]
            actual = r['deaths'][-days_to_correct]
            correction = actual - pred
            df_county['deaths'].values[i] = np.array([x if x < actual else int(x - correction) for x in r['deaths']])
    ndays = days_to_correct
    
def add_all_preds(df_county):
    """
    add single predictor predictions for the past {ndays} days
    """

    for method in methods:
        for t in tqdm(range(1, ndays + 1)):
            d = today - timedelta(t)
            if d < date(2020, 3, 16) and method in ['demographic']:
                continue 
            use_df = exponential_modeling.leave_t_day_out(df_county, 0 + t)

            if method != 'ensemble' and method != 'demographic':
                use_df = fit_and_predict.fit_and_predict(use_df, 
                                                 target_day=np.arange(1, horizon + 1),
                                                 outcome=outcome,
                                                 method=method,
                                                 mode='predict_future',
                                                 output_key=f'predicted_{outcome}_{method}_{horizon}')
            elif method == 'demographic':
                use_df = fit_and_predict.fit_and_predict(use_df, 
                                                 target_day=np.arange(1, horizon + 1),
                                                 outcome=outcome,
                                                 method='shared_exponential',
                                                 mode='predict_future',
                                                 demographic_vars=very_important_vars,
                                                 output_key=f'predicted_{outcome}_{method}_{horizon}') 
                
            df_county[f'all_{outcome}_pred_{d.month}_{d.day}_{method}_{horizon}'] = use_df[f'predicted_{outcome}_{method}_{horizon}']
     
    return df_county


def add_ensemble_prediction(df_county, month, day, outcome='deaths'):
    
    """
    add ensemble predictions made on given month and day, for the next {horizon} days
    
    Input:
        df_county: pd.DataFrame
        month: int
        day: int
        outcome: str
    
    Output: pd.DataFrame
        the ensemble predictions are saved in the column 'all_deaths_pred_{month}_{day}_ensemble_{horizon}'
        
    As an example, if month = 6 and day = 20, this function will add ensemble predictions 
    for 6/20, 6/21, ... 6/20 + horizon - 1,
    and the predictions are made based on data up to 6/19 (since the data on 6/19 is not available until 6/20)
    
    Note: this works only when previous 9 days' predictions of single predictors exist in the data frame df_county
    Otherwise, please use fit_and_predict_ensemble in fit_and_predict.py
    """    
    
    d0 = date(2020, month, day)
    delta_0 = (today - d0).days
    
    if d0 < date(2020, 3, 16):
        df_county[f'all_{outcome}_pred_{d0.month}_{d0.day}_ensemble_{horizon}'] = df_county[f'all_{outcome}_pred_{d0.month}_{d0.day}_linear_{horizon}'] 
        # before 3/16, the ensemble predictor is not available, because there was not enough data to train the expanded shared predictor; as such, we impute the ensemble predictions with linear predictions
        return df_county
    
    weights = {}
    for method in ['advanced_shared_model', 'linear']:
        y, y_preds = [], []
        for i in range(len(df_county)):
            y.append(df_county['deaths'].values[i][-(delta_0 + 7): -delta_0]) # actual deaths of last 7 days
            
            preds = []
            for k in range(7):
                d1 = d0 - timedelta(3+k)
                preds.append(df_county[f'all_{outcome}_pred_{d1.month}_{d1.day}_{method}_{horizon}'].values[i][2])
                # 3-day-ahead predicted deaths of last 7 days.
            y_preds.append(preds[::-1])
        y, y_preds = np.array(y), np.array(y_preds)
        weights[method] = pmdl_weight(np.sqrt(y), np.sqrt(np.maximum(y_preds, 0))) # compute weights
    
    ensemble_preds = []
    for i in range(len(df_county)):
        preds = np.zeros(horizon)
        for method in ['advanced_shared_model', 'linear']:
            preds += weights[method][i] * np.array(df_county[f'all_{outcome}_pred_{d0.month}_{d0.day}_{method}_{horizon}'].values[i])
        preds = preds/sum(weights[m][i] for m in ['advanced_shared_model', 'linear'])
        ensemble_preds.append(preds)
    df_county[f'all_{outcome}_pred_{d0.month}_{d0.day}_ensemble_{horizon}'] = ensemble_preds
    
    return df_county
    
def add_mepi(df_county, month, day, outcome='deaths'):
    
    """
    compute MEPI for given month and day for up to 14-day
    
    Input:
        df_county: pd.DataFrame
        month: int
        day: int
        outcome: str
    
    Output: pd.DataFrame
        the ensemble predictions are saved in the column 'all_deaths_pred_{month}_{day}_ensemble_mepi'
        
    As an example, if month = 6 and day = 20, this function will will add mepi for 6/20, 6/21, ... 7/3,
    and the mepi are made based on data up to 6/19 (since the data on 6/19 is not available until 6/20)
    
    Note: this only works when the ensemble predictions of last 19 days are available in df_county
    """    

    d0 = date(2020, month, day)
    mepis = []
    preds = df_county[f'all_{outcome}_pred_{month}_{day}_ensemble_{horizon}'].values
    for i in range(len(df_county)):
        pi_by_day = []
        d1 = d0 - timedelta(1)
        latest = df_county[f'#{outcome.capitalize()}_{d1.strftime("%m-%d-%Y")}'].values[i]
        for j in range(min(horizon, 14)): # add prediction intervals for up to 14 days ahead prediction
            me = 0
            for lb in range(5): # find max error of last 5 days
                d1 = d0 - timedelta(lb+1)
                d2 = d0 - timedelta(lb+j+1)
                actual = df_county[f'#{outcome.capitalize()}_{d1.strftime("%m-%d-%Y")}'].values[i]
                pred = df_county[f'all_{outcome}_pred_{d2.month}_{d2.day}_ensemble_{horizon}'].values[i][j]
                me = max(me, abs(actual/max(pred, 1)-1))
                #me = max(me, abs(actual-pred))
            pi_by_day.append((max(preds[i][j]*(1-me), latest), preds[i][j]*(1+me)))
            #pi_by_day.append((max(preds[i][j] - me, latest), preds[i][j] + me))
        mepis.append(pi_by_day)
    df_county[f'all_{outcome}_pred_{month}_{day}_ensemble_mepi'] = mepis
    
    return df_county


if __name__ == '__main__':
    '''
    Calculate a dataframe with all predictions
    predictions
        all_deaths_pred_month_day_ensemble_horizon
        this is a list of length horizon, first value is 1-day ahead prediction, second value is 2-day ahead prediction
        example: all_deaths_pred_3_27_ensemble_21
            list of length 21, first value is predictions made on 03/27 for 03/28, second value is predictions made on 03/27 for 03/28 and so on
    confidence intervals
        all_deaths_pred_month_day_ensemble_mepi - list of tuples corresponding to the predictions
    '''
    df_county = add_all_preds(df_county)  # add single predictor predictions
    #df_county.to_pickle("all_deaths_preds_6_21.pkl")
    for i in tqdm(range(1, ndays + 1)):   # add ensemble predictions
        d = today - timedelta(i)
        df_county = add_ensemble_prediction(df_county, d.month, d.day, 'deaths')
    for i in tqdm(range(1, ndays - 19)):  # add mepi
        d = today - timedelta(i)
        df_county = add_mepi(df_county, d.month, d.day, 'deaths')
            
    df_county.to_pickle("all_deaths_preds_6_21.pkl")


    
    print("computed all predictions successfully")
