import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import flask
import pandas as pd
import numpy as np
import time
import os, sys, inspect, json
from os.path import join as oj

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)
sys.path.append(rootdir)
sys.path.append(rootdir + '/modeling')
sys.path.append(rootdir + '/functions')

from fit_and_predict import add_preds
from viz import viz_map
import update_severity_index as severity_index
import load_data
import merge_data

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

data_dir = oj(rootdir, 'data')

# load in county data
df_county = load_data.load_county_level(data_dir=oj(rootdir, 'data'))
# add lat and lon to the dataframe
county_lat_lon = pd.read_csv(
    oj(rootdir, 'data/county_level/raw/county_ids/county_popcenters.csv'),
    dtype={'STATEFP': str, 'COUNTYFP': str}
)
county_lat_lon['fips'] = (county_lat_lon['STATEFP'] + county_lat_lon['COUNTYFP'])

# add predictions
NUM_DAYS_LIST = [1, 2, 3, 4, 5]
df_county = add_preds(df_county, NUM_DAYS_LIST=NUM_DAYS_LIST, cached_dir=data_dir)

# load in hospital data and merge
df_hospital = load_data.load_hospital_level(
    data_dir=oj(os.path.dirname(rootdir), 'covid-19-private-data')
)
df = merge_data.merge_county_and_hosp(df_county, df_hospital)
df = severity_index.add_severity_index(df, NUM_DAYS_LIST)

# load counties geojson
counties_json = json.load(open(oj(rootdir, 'data', 'geojson-counties-fips.json'), "r"))

# create hospital-level severity index plot
fig = viz_map.plot_hospital_severity_slider(
    df, target_days=np.array(NUM_DAYS_LIST),
    df_county=df_county, counties_json=counties_json, dark=True,
    auto_open=False, plot=False
)

app = dash.Dash('app', server=server)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

# county dropdown
app.layout = html.Div([
    html.H1('County'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Queens', 'value': 'Queens'},
            {'label': 'Kings', 'value': 'Kings'},
            {'label': 'Nassau', 'value': 'Nassau'}
        ],
        value='TSLA'
    ),
    dcc.Graph(figure=fig, id='my-graph')
], className="container")

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):

    fig = viz_map.plot_hospital_severity_slider(
        df, target_days=np.array(NUM_DAYS_LIST),
        df_county=df_county, counties_json=counties_json, dark=True,
        auto_open=False, plot=False,
        county_filter=selected_dropdown_value
    )

    return fig

if __name__ == '__main__':
    app.run_server()
