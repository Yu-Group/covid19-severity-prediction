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

    # add predictions
    NUM_DAYS_LIST = [1, 2, 3, 4, 5]
    df_county = add_preds(df_county, NUM_DAYS_LIST=NUM_DAYS_LIST, cached_dir=data_dir)

    deaths_fig = viz_map.plot_cumulative_deaths_map_with_slider(
        df_county, auto_open=False,
        target_days=np.array([0]+NUM_DAYS_LIST),
        filename=oj(parentdir, 'results', 'deaths.html')
    )
    print('successfully updated map of deaths')
    deaths_fig.write_image(oj(parentdir, 'results', 'deaths.png'),
                           width=900, height=600, scale=2)
    print('successfully updated png of map of deaths')

    # load in hospital data and merge
    df_hospital = load_data.load_hospital_level(
        data_dir=oj(os.path.dirname(parentdir), 'covid-19-private-data')
    )

    df = merge_data.merge_county_and_hosp(df_county, df_hospital)
    df = severity_index.add_severity_index(df, NUM_DAYS_LIST)

    # load counties geojson
    # counties_json = json.load(open(oj(parentdir, 'data', 'geojson-counties-fips.json'), "r"))

    # create hospital-level severity index plot
    severity_fig = viz_map.plot_hospital_severity_slider(
        df,
        target_days=np.array(NUM_DAYS_LIST),
        plot_choropleth=False,
        dark=True,
        auto_open=False,
        filename=oj(parentdir, 'results', 'severity_map.html')
    )
    print('successfully updated map of severity index')

    severity_fig.write_image(oj(parentdir, 'results', 'severity_map.png'),
                             width=900, height=600, scale=2)
    print('successfully updated png of map of severity index')
