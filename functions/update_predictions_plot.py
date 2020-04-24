import numpy as np
import pandas as pd
from os.path import join as oj
import os
import pygsheets
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
from viz import  viz_interactive, viz_static
import matplotlib.pyplot as plt
plt.switch_backend('agg')
plt.style.use('dark_background')
import plotly.express as px
import plotly

def predictions_plot(df_county, NUM_DAYS_LIST, num_days_in_past, output_key):
    today = datetime.today().strftime("%B %d")
    day_past = (datetime.now() - timedelta(days=num_days_in_past)).strftime("%B %d")
    df_county = df_county[df_county['tot_deaths'] >= 1]

    pred_key = f'Predicted deaths by {today}\n(predicted on {day_past})'
    deaths_key = f'Actual deaths by {today}'
    d = df_county.rename(columns={
        output_key: pred_key,
        'tot_deaths': deaths_key,
    })
    d = d[d[pred_key] >= 1e-1]
    minn = min(min(d[pred_key]), min(d[deaths_key])) + 1
    maxx = max(max(d[pred_key]), max(d[deaths_key]))

    px.colors.DEFAULT_PLOTLY_COLORS[:3] = ['rgb(239,138,98)','rgb(247,247,247)','rgb(103,169,207)']
    fig = px.scatter(d,
                     x=deaths_key, 
                     y=pred_key, 
                 size='PopulationEstimate2018',
                 hover_name="CountyName", 
                 hover_data=["CountyName", 'StateName'],
                 log_x=True, log_y=True)
    fig.update_layout(shapes=[
        dict(
          type= 'line',
          yref= 'y', y0=minn, y1=maxx,
          xref= 'x', x0=minn, x1=maxx,
          opacity=0.2
        )
    ])

    fig.update_layout(
                paper_bgcolor='rgba(0,0,0,255)',
                plot_bgcolor='rgba(0,0,0,255)',
                template='plotly_dark',
                title='County-level predictions'
            )
    plotly.offline.plot(fig, filename=oj(parentdir, 'results', 'predictions.html'), auto_open=False)
    
def forecasts_plot(df):
    R, C = 3, 1
    plt.figure(figsize=(8, 9))

    # top counties
    NUM_COUNTIES = 5
    dd = df.head(NUM_COUNTIES)
    plt.subplot(R, C, 1)
    viz_static.plot_forecasts(dd, death_thresh=16)
    plt.xlabel('')
    plt.title('Most-affected counties')

    # random
    dd = df[df.StateName != 'NY'] 
    plt.subplot(R, C, 2)
    viz_static.plot_forecasts(dd.head(6), death_thresh=16)
    plt.xlabel('')
    plt.title('Most-affected counties outside NY')


    # bay area
    bay_area = ['Alameda', 'Contra Costa', 'Lake', 'Marin', 'Mendocino', 'Napa', 'San Francisco', 
                'San Mateo', 'Santa Clara', 'Santa Cruz', 'Solano', 'Sonoma']
    dd = df[df.StateName == 'CA'] 
    dd = dd[dd.CountyName.isin(bay_area)]


    plt.subplot(R, C, 3)
    viz_static.plot_forecasts(dd.head(5), death_thresh=20)
    plt.title('Bay area counties')
    plt.tight_layout()
    plt.savefig(oj(parentdir, 'results', 'forecasts.svg'))
    
if __name__ == '__main__':
    print('loading data...')
    NUM_DAYS_LIST = [1, 2, 3, 4, 5, 6, 7]
    df_county = load_data.load_county_level(data_dir=oj(parentdir, 'data')).fillna(0)


    num_days_in_past = 3
    output_key = f'Predicted Deaths {num_days_in_past}-day Lagged'
    df_county = add_preds(df_county, NUM_DAYS_LIST=NUM_DAYS_LIST, cached_dir=oj(parentdir, 'data')) # adds keys like "Predicted Deaths 1-day"
    '''
    # don't use add_preds here, since we need preds from 3 days ago
    df_county = fit_and_predict_ensemble(df_county, 
                                outcome='deaths',
                                mode='eval_mode',
                                target_day=np.array([num_days_in_past]),
                                output_key=output_key)
    df_county[output_key] = [v[0] for v in df_county[output_key].values]
    '''
    predictions_plot(df_county, NUM_DAYS_LIST, num_days_in_past, output_key)
    
    forecasts_plot(df_county)
    print('succesfully updated prediction + forecast plots')