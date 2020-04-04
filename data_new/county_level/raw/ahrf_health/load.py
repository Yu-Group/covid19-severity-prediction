#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_ahrf_health(data_dir='./'):
    ''' Load in Area Health Resources Files (2018-2019 Release)
    
    Parameters
    ----------
    data_dir : str; path to the data directory with ahrf_health.csv
    
    Returns
    -------
    data frame
    '''
    
    raw = pd.read_csv(oj(data_dir, 'ahrf_health.csv'))
    return raw


if __name__ == '__main__':
    raw = load_ahrf_health()
    print('loaded ahrf_health successfully.')

