import numpy as np
from os.path import join as oj
import os
import pandas as pd
import sys
import inspect
from datetime import datetime, timedelta

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.path.append(parentdir + '/modeling')
import load_data
from fit_and_predict import add_preds
from viz import viz_interactive, viz_map_utils
import plotly
import re
import plotly.express as px
from urllib.request import urlopen
import json
import plotly.graph_objs as go
import pickle


## Load data and add prediction
def add_pre(df, var, name, newname):
    h = df_county[var + '1-day'].copy()
    for i in range(2, 8):
        h = np.vstack((h, df_county[var + str(i) + '-day']))
    df_county[name] = [h.T[i] for i in range(len(h.T))]





## Fill the state full name according to their abbreviations#
def fillstate(df):
    us_state_abbrev = {
        'AL': 'Alabama',
        'AK': 'Alaska',
        'AZ': 'Arizona',
        'AR': 'Arkansas',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'IA': 'Iowa',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'ME': 'Maine',
        'MD': 'Maryland',
        'MA': 'Massachusetts',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MS': 'Mississippi',
        'MO': 'Missouri',
        'MT': 'Montana',
        'NE': 'Nebraska',
        'NV': 'Nevada',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NY': 'New York',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VT': 'Vermont',
        'VA': 'Virginia',
        'WA': 'Washington',
        'WV': 'West Virginia',
        'WI': 'Wisconsin',
        'WY': 'Wyoming'
    }
    for i in range(df.shape[0]):
        if df.loc[i, "State"] not in us_state_abbrev.values():
            df.loc[i, "State"] = us_state_abbrev[df.loc[i, "StateName"]]

## Add cases/deaths rate to dataframe
def add_rates(df_county):
    for key in ['tot_deaths', 'tot_cases', 'new_deaths_last', 'new_cases_last']:
        df_county[key + '_rate'] = round(df_county[key] / df_county['PopulationEstimate2018'] * 100000, 2)


## Add new cases/deaths to dataframe
def add_new(df_county):
    def get_col_name(key, days):
        return '#' + key + '_' + (datetime.today() - timedelta(days=days)).strftime('%m-%d-%Y')

    for key in ['Cases', 'Deaths']:
        df_county['new_' + key.lower() + '_last'] = df_county[get_col_name(key, 1)] - df_county[get_col_name(key, 2)]
    for key in ['deaths', 'cases']:
        df_county['new_' + key] = [[] for _ in range(df_county.shape[0])]
        for i in range(df_county.shape[0]):
            df_county.loc[i, 'new_' + key].append(df_county.loc[i, key][0])
            for j in range(1, len(df_county.loc[i, key])):
                df_county.loc[i, 'new_' + key].append(df_county.loc[i, key][j] - df_county.loc[i, key][j - 1])


def add_new_pre(df_county, var, name, newname):
    h = df_county[var + '1-day'] - df_county[name]
    for i in range(2, 8):
        h = np.vstack((h, df_county[var + str(i) + '-day'] - df_county[var + str(i - 1) + '-day']))
    df_county[newname] = [h.T[i] for i in range(len(h.T))]
    df_county[newname + '_interval'] = [[] for _ in range(df_county.shape[0])]

    def find_intervals(b, a):
        tmp = [[a[0][0] - b, a[0][1] - b]]
        for i in range(1, len(a)):
            tmp.append([max(a[i][0] - a[i - 1][1], 0), max(a[i][1] - a[i - 1][0], 0)])
        return tmp

    for i in range(df_county.shape[0]):
        df_county.loc[i, newname + '_interval'].extend(
            find_intervals(df_county.loc[i, name], df_county.loc[i, var + 'Intervals']))
    return df_county
## Add prediction history to dataframe
def add_prediction_history(df_tab):
    def find_interval(a):
        return [max(a[6][0] - a[5][1], 0), max(a[6][1] - a[5][0], 0)]

    def add_predictions_7day(data, df):
        data = data.sort_values(by='countyFIPS')
        dic = {'cases': 'Cases', 'deaths': 'Deaths'}
        for i in range(df_tab.shape[0]):
            for key in dic.keys():
                df.loc[i, 'pred_7day_' + key].append(data.loc[i, 'Predicted ' + dic[key] + ' 7-day'])
                df.loc[i, 'pred_7day_' + key + '_interval'].append(
                    data.loc[i, 'Predicted ' + dic[key] + ' Intervals'][6])
                df.loc[i, 'pred_7day_new_' + key].append(max(0,
                                                             data.loc[i, 'Predicted ' + dic[key] + ' 7-day'] - data.loc[
                                                                 i, 'Predicted ' + dic[key] + ' 6-day']))
                df.loc[i, 'pred_7day_new_' + key + '_interval'].append(
                    find_interval(data.loc[i, 'Predicted ' + dic[key] + ' Intervals']))

    cached_dir = oj(parentdir, 'data')
    i = 0
    for c in ['deaths', 'cases']:
        for pre in ['pred_7day_', 'pred_7day_new_']:
            df_tab[pre + c] = [[] for _ in range(df_tab.shape[0])]
            df_tab[pre + c + '_interval'] = [[] for _ in range(df_tab.shape[0])]
    date2 = []
    k = 0
    while True:
        d = (datetime.today() - timedelta(days=i)).date()
        i += 1
        if cached_dir is not None:
            cached_fname = oj(cached_dir, f'preds_{d.month}_{d.day}_cached.pkl')
            if os.path.exists(cached_fname):
                date2.append(d + timedelta(days=6))
                add_predictions_7day(pd.read_pickle(cached_fname), df_tab)
            else:
                k += 1
                if k > 1:
                    break
    return df_tab, date2


if __name__ == '__main__':
    print('loading data...')
    NUM_DAYS_LIST = [1, 2, 3, 4, 5, 6, 7]
    df_county = load_data.load_county_level(data_dir=oj(parentdir, 'data')).fillna(0)
    df_county = add_preds(df_county, NUM_DAYS_LIST=NUM_DAYS_LIST,
                          cached_dir=oj(parentdir, 'data'))  # adds keys like "Predicted Deaths 1-day"

    ## orgnize predicts as array

    add_pre(df_county, 'Predicted Cases ', 'pred_cases', 'pred_new_cases')
    add_pre(df_county, 'Predicted Deaths ', 'pred_deaths', 'pred_new_deaths')

    ## add new cases/death to dataframe
    add_new(df_county)
    ## Add new cases/deaths predictions and their intervals 
    df_county = add_new_pre(df_county, 'Predicted Cases ', 'tot_cases', 'pred_new_cases')
    df_county = add_new_pre(df_county, 'Predicted Deaths ', 'tot_deaths', 'pred_new_deaths')

    ##fill missing values of some state full names
    fillstate(df_county)
    ## Add cases/deaths rate to the dataframe
    add_rates(df_county)
    ## Add past predictions
    df_county, past_dates = add_prediction_history(df_county)
    ## cache the results
    with open('functions/past_dates.pkl','wb') as f:
        pickle.dump(past_dates, f)
    df_county.to_pickle('functions/update_search.pkl')
