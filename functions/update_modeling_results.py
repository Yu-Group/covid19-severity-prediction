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
from fit_and_predict import fit_and_predict_ensemble
from functions import merge_data
from viz import  viz_interactive
import matplotlib.pyplot as plt
import plotly.express as px
import plotly

def predictions_plot(df_county, NUM_DAYS_LIST, num_days_in_past, output_key):
    today = datetime.today().strftime("%B %d")
    day_past = (datetime.now() - timedelta(days=num_days_in_past)).strftime("%B %d")


    pred_key = f'Predicted deaths by {today}\n(predicted on {day_past})'
    deaths_key = f'Actual deaths by {today}'
    d = df_county.rename(columns={
        output_key: pred_key,
        'tot_deaths': deaths_key,
    })
    minn = min(min(d[pred_key]), min(d[deaths_key])) + 1
    maxx = max(max(d[pred_key]), max(d[deaths_key]))


    fig = px.scatter(d,
                     x=pred_key, 
                     y=deaths_key, 
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
    
if __name__ == '__main__':
    print('loading data...')
    NUM_DAYS_LIST = [1, 2, 3, 4, 5, 6, 7]
    df_county = load_data.load_county_level(data_dir=oj(parentdir, 'data'))


    num_days_in_past = 3
    output_key = f'Predicted Deaths {num_days_in_past}-day'    
    df_county = fit_and_predict_ensemble(df_county, 
                                outcome='deaths',
                                mode='eval_mode',
                                target_day=np.array([num_days_in_past]),
                                output_key=output_key)
    df_county[output_key] = [v[0] for v in df_county[output_key].values]
    predictions_plot(df_county, NUM_DAYS_LIST, num_days_in_past, output_key)