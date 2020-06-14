## program for the search function 
import numpy as np
import pandas as pd
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
from functions import merge_data
from viz import  viz_interactive, viz_static, viz_map_utils
import plotly.figure_factory as ff
import plotly
import re


#Load data and add prediction
def add_pre(df, var, name):
    h = df_county[var + '1-day'].copy()
    for i in range(2,8):
        h = np.vstack((h,df_county[var + str(i) +'-day']))
    df_county[name] = [h.T[i] for i in range(len(h.T))]


# generate html for individual counties
def generate_all_counties():
    print('generating html for counties')
    df_tab = df_county[['CountyName', 'StateName', 
             'deaths', 'cases','countyFIPS','pred_cases','pred_deaths','Predicted Deaths Intervals','Predicted Cases Intervals']]
    df_tab = df_tab.rename(columns={'CountyName': 'County', 'StateName': 'State',
                                'Predicted Deaths Intervals': 'pred_deaths_interval',
                                'Predicted Cases Intervals': 'pred_cases_interval'})
    dates = viz_map_utils.date_in_data(df_county)
    viz_interactive.viz_curves_all_counties(df_tab, oj(parentdir, 'results/All_counties/'), dates)
    print('succesfully generated all county html')

# Generate map plot 
def generate_map():
    print('generating search map')
    fips = df_county['countyFIPS']
    values = df_county['tot_cases']
    binning = []
    level = 6
    for i in range(level):
        binning.append(np.rint(2**(np.log2(max(values))/(level+1)*(i+1))))
    fig = ff.create_choropleth(fips=fips, values=values,
                           colorscale = ['#F7E8E4','#F5C8BB','#B96D67','#A83C3B',
                                '#8B2222','#5B0D0D','#5A2318'],binning_endpoints=binning,
                           legend_title='Cases'
                          )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,255)',
        plot_bgcolor='rgba(0,0,0,255)',
        template='plotly_dark'
    )
    fig['layout'].update(width=1000, height=500, autosize=True)

    fig.write_image(oj(parentdir,"results/search_map.png"),width=900, height=450)
    
    print('succesfully generated search map')   
    
    return plotly.offline.plot(fig,
                include_plotlyjs='https://cdn.plot.ly/plotly-1.42.3.min.js',
                   output_type='div')


# update the html file (conbine search1 + search2 + search3)
def update_html(search2):
    id =re.search('<div id="([^ ]*)"',search2)
    print(id,id.group(1),id.group(0))
    with open(oj(parentdir,'results/search1.html'), 'r') as content_file:
        search1 = content_file.read()
    with open(oj(parentdir,'results/search3.html'), 'r') as content_file:
        search3 = content_file.read()
    f = open(oj(parentdir,'results/search.html'),"w+")
    f.write(search1+search2+search3.replace("map id to replace",id.group(1)))
    print('succesfully updated search html')

if __name__ == '__main__':
    print('loading data...')
    NUM_DAYS_LIST = [1, 2, 3, 4, 5, 6, 7]
    df_county = load_data.load_county_level(data_dir=oj(parentdir, 'data')).fillna(0)
    df_county = add_preds(df_county, NUM_DAYS_LIST=NUM_DAYS_LIST, cached_dir=oj(parentdir, 'data')) # adds keys like "Predicted Deaths 1-day"

    ## orgnize predicts as array
    add_pre(df_county,'Predicted Cases ','pred_cases')
    add_pre(df_county,'Predicted Deaths ','pred_deaths')

    generate_all_counties()
    search2 = generate_map()
    update_html(search2)
