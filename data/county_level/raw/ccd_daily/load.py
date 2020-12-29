#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_ccd_daily(data_dir='.'):
    ''' Load in COVID County Data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to write ccd_hospitalizations.csv
    
    Returns
    -------
    data frame
    '''
    
    # download data from source, which is updated daily
    cur_dir = os.getcwd()
    os.chdir(data_dir)
    os.system("wget https://api.covidcountydata.org/downloads/all_timeseries_latest.csv.zip -O ccd_daily.zip")
    os.system("unzip ccd_daily.zip")
    fcsv = [fname for fname in os.listdir() if fname.endswith(".csv") and fname != "ccd_daily.csv"][0]
    os.rename(fcsv, "ccd_daily.csv")
    os.remove("ccd_daily.zip")
    os.chdir(cur_dir)
    
    # load in data
    raw = pd.read_csv(oj(data_dir, "ccd_daily.csv"))
    
    return raw

if __name__ == '__main__':
    raw = load_ccd_daily()
    print('loaded ccd_daily successfully.')



