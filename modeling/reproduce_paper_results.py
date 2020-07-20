#!/usr/bin/python3

import sys
sys.path.append('../') 
#%load_ext autoreload
#%autoreload 2
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
import data_new
from datetime import datetime, timedelta, date

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

import fit_and_predict
import data_new
import warnings
warnings.filterwarnings("ignore")
import exponential_modeling
from collections import defaultdict
import os
from tqdm import tqdm

today = date(2020, 6, 21)
df_county = pd.read_pickle("all_deaths_preds_6_21.pkl")
label_name={'linear': 'linear', 'advanced_shared_model': 'expanded shared', 'ensemble': 'CLEP'}
color_name={'linear': 'darkred', 'advanced_shared_model': 'darkorange', 'ensemble': 'steelblue'}
ls_name={'linear': ':', 'advanced_shared_model': '--', 'ensemble': '-'}
all_methods = ['exponential', 'shared_exponential', 'demographic', 'advanced_shared_model', 'linear', 'ensemble']
all_metrics = ['mae', 'mape', 'sqrt']
result_dir = 'reproduce_paper_results/'
mepi_eval_period = {1: range(1, 42), 2: range(42, 72), 3: range(1, 72)}
error_num_days = 91
horizon = 21

def compute_prediction_errors(metric):
    """
    compute errors of different predictors from March 22 to Jun 20
    
    Input:
        metric: str
            one of all_metrics
            
    Output: 
        all_errors: dict
            for each method in all_methods, all_errors[method] is a dictionary
            for h = 1, 2, ..., 21, all_errors[method][h] is a list of previous prediciton errors
        all_dates: list
            all dates from March 22 to Jun 20, in MM/DD format
    """
    
    all_dates = []
    all_errors = defaultdict(list)
    for method in all_methods:
        all_errors[method] = defaultdict(list) 
        
    for td in range(1, 22):
        for i in range(1, error_num_days + 1):
            d1 = today - timedelta(i)
            d2 = today - timedelta(i+td-1)
            all_dates.append(f'{d1.month}/{d1.day}')
            actual = np.array([p[-i] for p in df_county['deaths'].values])
            for method in all_methods:
                preds_key = f'all_deaths_pred_{d2.month}_{d2.day}_{method}_{horizon}'
                if preds_key in df_county:
                    preds = np.array([p[td-horizon-1] for p in df_county[preds_key]])
                    y = actual[actual>=10]
                    y_preds = preds[actual>=10]
                    if metric == 'mae':
                        err = y - y_preds
                    elif metric == 'mape':
                        err = (y - y_preds)/np.maximum(y, 1)
                    elif metric == 'sqrt':
                        err = np.sqrt(y) - np.sqrt(np.abs(y_preds))
                    all_errors[method][td].append(np.mean(np.abs(err)))
                else:
                    all_errors[method][td].append(np.nan)
    all_dates = np.array(all_dates)
                    
    return all_errors, all_dates

def print_prediction_error_quantiles(metric, all_errors):
    
    """
    Print Table 4 in the paper
    """

    quantiles = defaultdict(list)
    for td in [3, 5, 7, 14]:
        for qt in [10, 50, 90]:
            colname = f'{td}_day_{qt}'
            for method in all_methods:
                quantiles[colname].append(np.nanquantile(all_errors[method][td], qt/100.0))
    res_df = pd.DataFrame(quantiles, index=['separate', 
                                            'shared', 
                                            'demographics',
                                            'expanded shared', 
                                            'linear', 
                                            'ensemble'])
    filename = os.path.join(result_dir, f'{metric}_error_quantiles.csv')
    res_df.to_csv(filename)
    

def plot_7_day_prediction_errors(metric, all_errors, all_dates):
    
    """
    Plot Figure 6 in the paper
    """        
    plt.figure(figsize=(4, 3), dpi=200)
    ax = plt.subplot(111)
    for method in ['linear', 'advanced_shared_model', 'ensemble']:
        if method != 'ensemble':
            ax.plot(all_errors[method][7][::-1], 
                    label=label_name[method], 
                    color=color_name[method], 
                    linestyle=ls_name[method],
                    linewidth=2.5, 
                    alpha=.66)
        else:
            ax.plot(all_errors[method][7][::-1], 
                    label=label_name[method], 
                    color=color_name[method], 
                    linestyle=ls_name[method],
                    linewidth=2.5)
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    if metric == 'mae':
        plt.ylabel("Raw scale MAE", fontsize=15)
    elif metric == 'mape':
        plt.ylabel("MAPE", fontsize=15)
    elif metric == 'sqrt':
        plt.ylabel("Square root scale MAE", fontsize=15)
    plt.yticks([20, 40, 60], fontsize=12)
    plt.xticks(fontsize=12)
    plt.xticks(range(0, error_num_days, 14), all_dates[::-1][range(0, error_num_days, 14)])
    plt.xlabel("Date", fontsize=15)
    plt.tight_layout()
    filename = os.path.join(result_dir, f'over_time_{metric}_jun21.pdf')
    plt.savefig(filename)
    
def plot_7_10_14_day_clep_errors(metric, all_errors, all_dates):
    
    """
    Plot Figure 7 and Figure 8 (a)-(c) in the paper
    """     
    
    plt.figure(figsize=(4, 3), dpi=200)
    ax = plt.subplot(111)
    color_name_by_td = {7:'darkred', 10:'darkorange', 14: 'steelblue'}
    ls_name_by_td ={7:':', 10:'--', 14: '-'}
    for td in [7, 10, 14]:
        plt.plot(all_errors['ensemble'][td][:71][::-1], 
                 label=f'{td} day', 
                 linestyle=ls_name_by_td[td], 
                 color=color_name_by_td[td], 
                 linewidth=2.5) 
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    if metric == 'mae':
        plt.ylabel("Raw scale MAE", fontsize=15)
    elif metric == 'mape':
        plt.ylabel("MAPE", fontsize=15)
    elif metric == 'sqrt':
        plt.ylabel("Square root scale MAE", fontsize=15)
    plt.xlabel("Date", fontsize=15)
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.xticks(range(0, 70, 11), all_dates[np.arange(0, 70, 11)][::-1])
    plt.legend(fontsize=12)
    plt.tight_layout()
    filename = os.path.join(result_dir, f'{metric}_clep_14_day.pdf')
    plt.savefig(filename)
    
    plt.figure(figsize=(4, 3), dpi=200)
    ax = plt.subplot(111)
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    plt.boxplot([all_errors['ensemble'][td][:71] for td in [3, 5, 7, 10, 14]])
    plt.yscale('linear')
    plt.ylabel("MAPE (%)", fontsize=15)
    plt.xlabel("Horizon", fontsize=15)
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    plt.xticks([1, 2, 3, 4, 5], [3, 5, 7, 10, 14])
    plt.tight_layout()
    filename = os.path.join(result_dir, f'{metric}_clep_box_plot.pdf')
    plt.savefig(filename)
    
def plot_clep_median_error(metric, all_errors):

    """
    Plot Figure 8 (d)-(f) in the paper
    """  
    
    median_error = []
    for td in range(1, 22):
        median_error.append(np.median(all_errors['ensemble'][td]))
    plt.figure(figsize=(4, 3), dpi=200)
    ax = plt.subplot(111)
    plt.plot(np.arange(1, 22, 1), median_error, color='lightcoral', linewidth=3)
    plt.ylabel("Median of MAPE (%)", fontsize=15)
    plt.xlabel("Horizon", fontsize=15)
    plt.yticks(fontsize=12)
    plt.xticks(fontsize=12)
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)
    plt.xticks([1, 6, 11, 16, 21])
    plt.tight_layout()
    filename = os.path.join(result_dir, f'median_{metric}_clep_21_day.pdf')
    plt.savefig(filename)
    
    
def print_and_plot_all_prediction_errors():
    
    """
    produce all tables and plots related to CLEP performance
    """  
    
    for metric in all_metrics:
        all_errors, all_dates = compute_prediction_errors(metric)
        print_prediction_error_quantiles(metric, all_errors)
        plot_7_day_prediction_errors(metric, all_errors, all_dates)
        plot_7_10_14_day_clep_errors(metric, all_errors, all_dates)
        plot_clep_median_error(metric, all_errors)
        
    
def county_level_results(counties, td):
    
    """
    plot Figure 9 and 10 in the paper
    """
    
    df_county['CountyNamew/StateAbbrev'] = [df_county['CountyName'].iloc[i] + ', ' + df_county['StateName'].iloc[i] for i in range(len(df_county))]
    random1 = ['Bergen, NJ', 'Broward, FL', 'Dougherty, GA', 'Monmouth, NJ', 'Oakland, MI', 'Suffolk, NY']
    random_index = np.where(df_county['CountyNamew/StateAbbrev'].isin(random1) == True)[0]
    
    R, C = 2, 3
    fig = plt.figure(figsize=(9, 4), dpi=400)
    for i in range(R * C):
        ax = plt.subplot(R, C, i + 1)
        #ax = fig.add_subplot(3, 2, i+1)
        if counties == 'worst':
            r = df_county.iloc[i]
        elif counties == 'random':
            r = df_county.iloc[random_index[i]]
        ax.spines["top"].set_visible(False)  
        ax.spines["right"].set_visible(False)
        #num = r['deaths']
        plt.title(r['CountyName'] + ' County, ' + r['StateName'], fontsize=10)
        actual, pred, mepi, dates = [], [], [], []
        for j in range(1, 72):
            d0 = today - timedelta(j)
            d1 = d0 - timedelta(td-1)
            dates.append(f'{d0.month}/{d0.day}')
            actual.append(r[f'#{outcome.capitalize()}_{d0.strftime("%m-%d-%Y")}'])
            mepi.append(r[f'all_{outcome}_pred_{d1.month}_{d1.day}_ensemble_mepi'][td-1])
            pred.append(r[f'all_{outcome}_pred_{d1.month}_{d1.day}_ensemble_{horizon}'][td-1])
        plt.plot(actual[::-1], label='Recorded deaths', color='black')
        plt.plot(pred[::-1], label=f'{td}-day predictions', linestyle='--', color='steelblue')
        plt.fill_between(range(71), 
                         [p[0] for p in mepi][::-1], 
                         [p[1] for p in mepi][::-1], 
                         #color='r', 
                         alpha=.15,
                         color='steelblue',
                         label='Prediction intervals'
                         )
        plt.grid(which='major', linestyle='--', linewidth=.5, alpha=.5)
        plt.xticks(range(0, 71, 11), np.array(dates)[::-1][range(0, 71, 11)], fontsize=8)
        plt.yticks(fontsize=8)
        #plt.ylim((0, 5 * np.max(actual)))
        if td == 14:
            plt.ylim((0, min(20000, np.max(mepi))))
        if i==0:
            plt.legend(loc='lower right', fontsize=6)

    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    plt.xlabel("Date")
    plt.ylabel("Cumulative deaths")
    plt.tight_layout()
    filename = os.path.join(result_dir, f'{counties}_counties_jun21_{td}_day.pdf')
    plt.savefig(filename)
    
def plot_all_county_level_results():

    """
    produce all county-level CLEP and MEPI results (Figures 9 and 10)
    """
    
    for counties in ['worst', 'random']:
        for td in [7, 14]:
            county_level_results(counties, td)
    
def mepi_results(td, period):
    
    """
    compute mepi coverage and performance, and plot Figure 11 and 12 in the paper
    """
    
    avg_coverage = np.zeros(len(df_county))
    avg_length = np.zeros(len(df_county))
    ndays = np.zeros(len(df_county))
    for i in range(len(df_county)):
        for j in mepi_eval_period[period]:
            d0 = today - timedelta(j)
            d1 = d0 - timedelta(td-1)
            actual = df_county[f'#Deaths_{d0.strftime("%m-%d-%Y")}'].values[i]
            mepi = df_county[f'all_deaths_pred_{d1.month}_{d1.day}_ensemble_mepi'].values[i][td-1]
            if period != 3 or (period == 3 and actual >= 10):
                avg_coverage[i] += (int((mepi[0])) <= actual <= int((mepi[1])))
                avg_length[i] += (int((mepi[1]))-int((mepi[0])))/max(actual, 1)
                ndays[i] += 1    
    
    plt.figure(figsize=(4, 3), dpi=200) 
    x = np.array(avg_coverage[ndays >= 10])/ndays[ndays >= 10]*100
    ax = plt.subplot(111)  
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    plt.xticks(fontsize=18)
    plt.xlabel("Coverage %", fontsize=14)  
    plt.ylabel("Count", fontsize=14) 
    plt.hist(x,  
             color="#3F5D7D", bins=15)
    #plt.title("Histogram of coverage", fontsize=14)
    plt.xlim((0, 105))
    plt.tight_layout()
    filename = os.path.join(result_dir, f'mepi_coverage_period_{period}_{td}_day.pdf')
    plt.savefig(filename)
    
    
    plt.figure(figsize=(4, 3), dpi=200) 
    x = np.array(avg_length[ndays >= 10])/ndays[ndays >= 10]
    ax = plt.subplot(111)  
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
    plt.xticks(fontsize=18)
    plt.xlabel("Average normalized length", fontsize=14)  
    plt.ylabel("Count", fontsize=14) 
    plt.hist(x[x<12],  
             color="#3F5D7D", bins=50)
    if td == 14:
        plt.xlim((0, 12))
        plt.xticks([2.0, 4.0, 6.0, 8.0, 10.0])
    if td == 7:
        plt.xlim((0, 5))
        plt.xticks([1, 2, 3, 4])
    #plt.xticks([2.0, 4.0, 6.0])
    plt.tight_layout()
    filename = os.path.join(result_dir, f'mepi_length_period_{period}_{td}_day.pdf')
    plt.savefig(filename)

def plot_all_mepi_results():    

    """
    produce all MEPI-related results
    """
    for period in [1, 2, 3]:
        for td in [7, 14]:
            mepi_results(td, period)    
    
if __name__ == '__main__':
    
    print_and_plot_all_prediction_errors()
    plot_all_county_level_results()
    plot_all_mepi_results()
