import sys, os, inspect
from os.path import join as oj
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.path.append(parentdir + '/modeling')
sys.path.append(parentdir + '/viz')

from fit_and_predict import add_preds
from viz_interactive import plot_counties_slider
import load_data
import numpy as np
import pandas as pd

if __name__ == "__main__":
    data_dir = oj(parentdir, 'data')
    # load in county data
    df = load_data.load_county_level(data_dir=oj(parentdir, 'data'))
    # add lat and lon to the dataframe
    county_lat_lon = pd.read_csv(
        oj(data_dir, 'county_pop_centers.csv'),
        dtype={'STATEFP': str, 'COUNTYFP': str}
    )
    county_lat_lon['fips'] = (county_lat_lon['STATEFP'] + county_lat_lon['COUNTYFP']).astype(np.int64)
    # add predictions
    df = add_preds(df, NUM_DAYS_LIST=[1, 2, 3], cached_dir=data_dir)
    # join lat / lon to df
    df = df.join(county_lat_lon.set_index('fips'), on='countyFIPS', how='left').rename(
        columns={'LATITUDE': 'lat', 'LONGITUDE': 'lon'}
    )
    # create plot
    plot_counties_slider(df, auto_open=False,
                         n_past_days=1,
                         target_days=np.array([1, 2, 3]),
                         filename=oj(parentdir, 'results', 'deaths.html'))
