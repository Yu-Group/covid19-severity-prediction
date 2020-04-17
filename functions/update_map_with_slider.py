import sys, os, inspect, json
from os.path import join as oj
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.path.append(parentdir + '/modeling')
# sys.path.append(parentdir + '/viz')

from fit_and_predict import add_preds
from viz import viz_map
import update_severity_index as severity_index
import load_data
import merge_data
import numpy as np
import pandas as pd

if __name__ == "__main__":
    data_dir = oj(parentdir, 'data')
    # load in county data
    df_county = load_data.load_county_level(data_dir=oj(parentdir, 'data'))
    # add lat and lon to the dataframe
    county_lat_lon = pd.read_csv(
        oj(parentdir, 'data_old/county_pop_centers.csv'),
        dtype={'STATEFP': str, 'COUNTYFP': str}
    )
    county_lat_lon['fips'] = (county_lat_lon['STATEFP'] + county_lat_lon['COUNTYFP'])#.astype(np.int64)
    # add predictions
    NUM_DAYS_LIST = [1, 2, 3, 4, 5]
    df_county = add_preds(df_county, NUM_DAYS_LIST=NUM_DAYS_LIST, cached_dir=data_dir)
    # join lat / lon to df_county
    # This does not seem necessary as lat and lon is already in the df_county
    #df_county = df_county.join(county_lat_lon.set_index('fips'), on='countyFIPS', how='left').rename(
    #    columns={'LATITUDE': 'lat', 'LONGITUDE': 'lon'}
    #)
    # create county-level predictions plot
    viz_map.plot_counties_slider(df_county, auto_open=False,
                         n_past_days=1,
                         target_days=np.array(NUM_DAYS_LIST),
                         filename=oj(parentdir, 'results', 'deaths.html'))

    # load in hospital data and merge
    df_hospital = load_data.load_hospital_level(data_dir=oj(parentdir, 'data_hospital_level'))
    df = merge_data.merge_county_and_hosp(df_county, df_hospital)
    df = severity_index.add_severity_index(df, NUM_DAYS_LIST)

    # load counties geojson
    counties_json = json.load(open(oj(parentdir, 'data', 'geojson-counties-fips.json'), "r"))

    # create hospital-level severity index plot
    viz_map.plot_hospital_severity_slider(
        df, target_days=np.array(NUM_DAYS_LIST),
        df_county=df_county, counties_json=counties_json, dark=True,
        auto_open=False, filename=oj(parentdir, 'results', 'severity_map.html')
    )
