import numpy as np
import pandas as pd
from os.path import join as oj
import pygsheets
import pandas as pd
import sys
sys.path.append('../modeling')
sys.path.append('..')
import load_data
from fit_and_predict import add_preds
from functions import merge_data

if __name__ == '__main__':
    NUM_DAYS_LIST = [1]
    df_county = load_data.load_county_level(data_dir='../data')
    df_hospital = load_data.load_hospital_level(data_dir='../data_hospital_level')
    df_county = add_preds(df_county, NUM_DAYS_LIST=NUM_DAYS_LIST) # adds keys like "Predicted Deaths 1-day"
    print('succesfully ran pipeline!')


