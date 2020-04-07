import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
sys.path.append(parentdir + '/modeling')

from modeling import fit_and_predict
from fit_and_predict import add_preds
from viz_interactive import plot_counties_slider
import load_data
import pandas as pd

data_dir = sys.argv[1]
lat_lon_file = sys.argv[2]

# usage: python update_slider.py data_dir county_lat_long.csv

if __name__ == "__main__":
    df = load_data.load_county_level()
    county_lat_lon = pd.read_csv(data_dir + '/' + lat_lon_file)
    df = add_preds(df, NUM_DAYS_LIST=[1, 2, 3], cached_dir=data_dir)
    df = df.join(county_lat_lon.set_index('fips'), on='countyFIPS', how='left')
    plot_counties_slider(df)
