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
from viz import viz_interactive, viz_map_utils
import plotly
import re
import plotly.express as px
from urllib.request import urlopen
import json
import plotly.graph_objs as go
import pickle


# generate html for individual counties
def generate_all_counties(df, past_dates):
    print('generating html for counties')
    df = df.rename(columns={'CountyName': 'County', 'State': 'State',
                                    'Predicted Deaths Intervals': 'pred_deaths_interval',
                                    'Predicted Cases Intervals': 'pred_cases_interval'})
    dates = viz_map_utils.date_in_data(df)
    viz_interactive.viz_curves_all_counties(df, oj(parentdir, 'results/All_counties/'), dates, past_dates)
    print('succesfully generated all county html')


## Rename columns
def rename(df):
    return df.rename(columns={"tot_deaths": "Cumulative Deaths", "tot_cases": "Cumulative Cases",
                              "new_cases_last": "New Cases", "new_deaths_last": "New Deaths",
                              'CountyName': 'County', 'tot_deaths_rate': 'Deaths per 100k',
                              'tot_cases_rate': 'Cases per 100k', 'new_cases_last_rate': 'New Cases per 100k',
                              'new_deaths_last_rate': 'New Deaths per 100k'})


# Generate map and table html code
def generate_map(df, keys):
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
## update search.html
def update_html(maps,keys):
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


if __name__ == '__main__':
    print('loading data...')
    with open('functions/past_dates.pkl','rb') as f:
        past_dates = pickle.load(f)
    df_county = pd.read_pickle('functions/update_search.pkl')
    ## generate plots for all counties
    #generate_all_counties(df_county, past_dates)
    ## keys for the tab and map
    keys = ['Cumulative Cases', 'Cumulative Deaths', 'New Cases', 'New Deaths', 'Cases per 100k', 'Deaths per 100k',
            'New Cases per 100k', 'New Deaths per 100k']
    ## generate maps in different tabs
    #maps = generate_map(df_county,keys)
    ## update html of search.html
    #update_html(maps, keys)
