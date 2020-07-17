#!/usr/bin/python3

import sys
sys.path.append('../') 
sys.path.append('../data') 
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
import data as data_new
from datetime import datetime, timedelta, date

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

import fit_and_predict
# import data_new
import warnings
warnings.filterwarnings("ignore")
import exponential_modeling
from pmdl_weight import pmdl_weight

from tqdm import tqdm

ndays = 99
outcome = 'deaths'
horizon = 21

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
methods = ['linear', 'advanced_shared_model', 'shared_exponential', 
           'demographic', 'exponential']
advanced_model = {'model_type':'advanced_shared_model'}
linear = {'model_type':'linear'}
corrected = False
df_county = load_data.load_county_level(data_dir = '../data/')
today = date(2020, 6, 21) # this should be one day after the last date in df_county
#df_county = pd.read_pickle("all_cases_preds_6_21.pkl")

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
            d = today - timedelta(t)
            df_county[f'all_{outcome}_pred_{d.month}_{d.day}_{method}_{horizon}'] = use_df[f'predicted_{outcome}_{method}_{horizon}']
     
    return df_county


def add_ensemble_prediction(df_county, month, day, outcome='deaths', days_ahead: int=3):
    """
    add ensemble predictions made on given month and day
    for example, if month = 6 and day = 20, this function will add ensemble predictions for 6/20, 6/21, ... 6/20 + horizon - 1,
    and the predictions are made based on data up to 6/19 (since the data on 6/19 is not available until 6/20)
    this works only when previous (9) days' predictions of single predictors exist in the data frame df_county
    Params
    ------
    days_ahead
        Number of days in the future to predict
    
    the ensemble predictions are saved in the column 'all_deaths_pred_{month}_{day}_ensemble_{horizon}'
    """    
    d0 = date(2020, month, day)
    delta_0 = (today - d0).days
    
    weights = {}
    for method in ['advanced_shared_model', 'linear']:
        y, y_preds = [], []
        for i in range(len(df_county)):
            y.append(df_county['deaths'].values[i][-(delta_0 + 7): -delta_0]) # actual deaths of last 7 days
            
            preds = []
            for k in range(7):
                d1 = d0 - timedelta(3+k)
                preds.append(df_county[f'all_{outcome}_pred_{d1.month}_{d1.day}_{method}_{horizon}'].values[i][days_ahead - 3])
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
    for example, if month = 6 and day = 20, this function will add mepi for 6/20, 6/21, ... 7/3,
    only works when the ensemble predictions of last 19 days are available in df_county
    
    the ensemble predictions are saved in the column 'all_deaths_pred_{month}_{day}_ensemble_mepi'
    """
    d0 = date(2020, month, day)
    mepis = []
    preds = df_county[f'all_{outcome}_pred_{month}_{day}_ensemble_{horizon}'].values
    for i in range(len(df_county)):
        pi_by_day = []
        d1 = d0 - timedelta(1)
        latest = df_county[f'#{outcome.capitalize()}_{d1.strftime("%m-%d-%Y")}'].values[i]
        for j in range(14): # add prediction intervals for up to 14 days ahead prediction
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
    
    df_county = add_all_preds(df_county)  
    days_ahead = 7
    for i in tqdm(range(1, ndays - 10)):
        d = today - timedelta(i)
        df_county = add_ensemble_prediction(df_county, d.month, d.day, 'deaths', days_ahead=days_ahead)
    '''
    for i in tqdm(range(1, ndays - 24)):
        d = today - timedelta(i)
        df_county = add_mepi(df_county, d.month, d.day, 'deaths')     
    df_county.to_pickle("all_deaths_preds_6_21.pkl")
    '''
    
    df_county.to_csv(f'all_deaths_preds_{days_ahead}.csv')
    
    print("computed all predictions successfully")
        
