#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_unacast_mobility(data_dir='.'):
    ''' Load in Unacast Social Mobility and Distancing data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to write unacast_mobility.csv
    
    Returns
    -------
    data frame
    '''
    
    # load in data
    raw = pd.read_csv(oj(data_dir, "unacast_mobility.csv"))
    
    return raw

if __name__ == '__main__':
    raw = load_unacast_mobility()
    print('loaded unacast_mobility successfully.')


