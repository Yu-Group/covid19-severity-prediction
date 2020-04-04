#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_dhdsp_heart(data_dir='.'):
    ''' Load in CDC DHDSP heart disease mortality data
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing dhdsp_heart.csv
    
    Returns
    -------
    data frame
    '''
    
    # load in data
    raw = pd.read_csv(oj(data_dir, "dhdsp_heart.csv"), 
                      na_values = [-1, -9999, ""])
    return raw

if __name__ == '__main__':
    raw = load_dhdsp_heart()
    print('loaded dhdsp_heart successfully.')

