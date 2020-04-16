#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_cdc_svi(data_dir='.'):
    ''' Load in CDC Social Vulnerability Index data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to write cdc_svi.csv
    
    Returns
    -------
    data frame
    '''
    
    # load in data
    raw = pd.read_csv(oj(data_dir, "cdc_svi.csv"), na_values = [-999])
    
    return raw

if __name__ == '__main__':
    raw = load_cdc_svi()
    print('loaded cdc_svi successfully.')



