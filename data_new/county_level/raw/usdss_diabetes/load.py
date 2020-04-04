#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_usdss_diabetes(data_dir='.'):
    ''' Load in USDSS Diagnosed Diabetes data
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing usdss_diabetes.csv
    
    Returns
    -------
    data frame
    '''
    
    # load in data
    raw = pd.read_csv(oj(data_dir, "usdss_diabetes.csv"), 
                      skiprows = 2, 
                      na_values = ['No Data'])
    raw = raw.dropna(subset = ["CountyFIPS"])
    
    return raw

if __name__ == '__main__':
    raw = load_usdss_diabetes()
    print('loaded usdss_diabetes successfully.')


