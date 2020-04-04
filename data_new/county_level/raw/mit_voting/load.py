#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_mit_voting(data_dir='.'):
    ''' Load in 2000-2016 County Presidential Data
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing mit_voting.csv
    
    Returns
    -------
    data frame
    '''
    raw = pd.read_csv(oj(data_dir, 'mit_voting.csv'))
    
    return raw

if __name__ == '__main__':
    raw = load_mit_voting()
    print('loaded mit_voting successfully.')



