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


# Load data and add prediction
def add_pre(df, var, name, newname):
    h = df_county[var + '1-day'].copy()
    for i in range(2, 8):
        h = np.vstack((h, df_county[var + str(i) + '-day']))
    df_county[name] = [h.T[i] for i in range(len(h.T))]


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


# generate html for individual counties
def generate_all_counties():
    print('generating html for counties')
    df_tab = df_county[['CountyName', 'State', 'new_cases', 'new_deaths',
                        'deaths', 'cases', 'countyFIPS', 'pred_cases', 'pred_deaths', 'Predicted Deaths Intervals',
                        'Predicted Cases Intervals',
                        'pred_new_cases', 'pred_new_deaths', 'pred_new_cases_interval', 'pred_new_deaths_interval']]
    df_tab = df_tab.rename(columns={'CountyName': 'County', 'State': 'State',
                                    'Predicted Deaths Intervals': 'pred_deaths_interval',
                                    'Predicted Cases Intervals': 'pred_cases_interval'})
    dates = viz_map_utils.date_in_data(df_county)
    df_tab, date2 = add_prediction_history(df_tab)
    viz_interactive.viz_curves_all_counties(df_tab, oj(parentdir, 'results/All_counties/'), dates, date2)
    print('succesfully generated all county html')


## Rename columns
def rename(df):
    return df.rename(columns={"tot_deaths": "Cumulative Deaths", "tot_cases": "Cumulative Cases",
                              "new_cases_last": "New Cases", "new_deaths_last": "New Deaths",
                              'CountyName': 'County', 'tot_deaths_rate': 'Deaths per 100k',
                              'tot_cases_rate': 'Cases per 100k', 'new_cases_last_rate': 'New Cases per 100k',
                              'new_deaths_last_rate': 'New Deaths per 100k'})


# Generate map and table html code
def generate_map(df):
    df = rename(df)
    df['POS'] = df['County'] + ', ' + df['StateName']
    maps = []
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)
    for key in keys:
        fig = px.choropleth(df, geojson=counties, locations='countyFIPS', color=np.log(df[key] + 1),
                            color_continuous_scale=['#F7E8E4', '#F5C8BB', '#B96D67', '#A83C3B',
                                                    '#8B2222', '#5B0D0D', '#5A2318'],
                            scope="usa",
                            hover_data=['State', 'County', 'Cumulative Cases', 'New Cases', 'Cumulative Deaths'
                                , 'New Deaths', 'Deaths per 100k', 'Cases per 100k', 'New Cases per 100k',
                                        'New Deaths per 100k'],
                            title=key + ' on ' + (datetime.today() - timedelta(days=1)).strftime('%m-%d'))
        fig.update_layout(coloraxis_colorbar=dict(len=0.75,
                                                  title=key,
                                                  tickvals=[2.302585092994046, 4.605170185988092, 6.907755278982137,
                                                            9.210340371976184, 11.512925464970229],
                                                  ticktext=['10', '100', '1k', '10k', '100k', '1000k'],
                                                  x=1, y=0.5))
        ## update the hover information
        for c in ["countyFIPS=%{location}<br>", "<br>color=%{z}"]:
            fig['data'][0]['hovertemplate'] = fig['data'][0]['hovertemplate'].replace(c, "")
        fig['data'][0]['hovertemplate'] = fig['data'][0]['hovertemplate'].replace("=", ": ")
        fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
        fig.update_layout(
            paper_bgcolor='rgb(0,0,0)',
            plot_bgcolor='rgb(0,0,0)',
            template='plotly_dark',
        )
        fig['layout'].update(width=900, height=450, autosize=True, title_x=0.3)
        if key == 'Cumulative Cases':
            fig.write_image(oj(parentdir,"results/search_map.svg"),width=900, height=450)
        maps.append(plotly.offline.plot(fig,include_plotlyjs=False,output_type='div'))
    
        df_tab = df.sort_values(by = key, ascending = False)
        df_tab = df_tab.reset_index(drop=True)[['POS',key]].loc[:19,:]
        fig = go.Figure(data=[go.Table(
            header=dict(values=['', 'County', key],
                        line_color='grey',
                        fill_color='darkgrey',
                        font_color='white',
                        font_size=12,
                        align='center'),
            cells=dict(values=[[i + 1 for i in range(len(df_tab))],
                               df_tab['POS'],
                               df_tab[key]],
                       line_color='darkgrey',
                       fill_color='grey',
                       font_color='white',
                       font_size=11,
                       align='center'),
            columnwidth=[20, 120, 80])
        ])
        fig['layout'].update(paper_bgcolor='rgb(0,0,0)',
                                plot_bgcolor='rgb(0,0,0)',
                                margin=dict(l=0, r=0, t=0, b=0),
                                width=200, height=550, autosize=True,
                                template='plotly_dark')
        fig.write_image(oj(parentdir,"results/" + key + ".svg"),width=200, height=550)
    print('succesfully generated search map')
    return maps


# Fill the state full name according to their abbreviations#
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


## update search.html
def update_html(maps):
    f = open(oj(parentdir, 'results/template.html'), "r")
    content = f.read()
    for i, key in enumerate(keys):
        content = content.replace(key + ' map', maps[i], 1)
        id = re.search('<div id="([^ ]*)"', maps[i])
        content = content.replace(key + " id to replace", id.group(1), 1)
    f = open(oj(parentdir, 'results/search.html'), "w+")
    f.write(content)
    print('succesfully updated search html')


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


if __name__ == '__main__':
    print('loading data...')
    NUM_DAYS_LIST = [1, 2, 3, 4, 5, 6, 7]
    df_county = load_data.load_county_level(data_dir=oj(parentdir, 'data')).fillna(0)
    df_county = add_preds(df_county, NUM_DAYS_LIST=NUM_DAYS_LIST,
                          cached_dir=oj(parentdir, 'data'))  # adds keys like "Predicted Deaths 1-day"
    df_county.loc[2409,'PopulationEstimate2018'] = 13586

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
    generate_all_counties()
    ## keys for the tab and map
    keys = ['Cumulative Cases', 'Cumulative Deaths', 'New Cases', 'New Deaths', 'Cases per 100k', 'Deaths per 100k',
            'New Cases per 100k', 'New Deaths per 100k']
    ## generate maps in different tabs
    maps = generate_map(df_county)
    ## update html of search.html
    update_html(maps)
