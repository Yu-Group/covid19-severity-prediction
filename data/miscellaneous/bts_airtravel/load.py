#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_bts_airtravel(data_dir='.'):
    ''' Load in Airline Origin and Destination Survey (DB1B) (2019)
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing 
               ./quarter_data/bts_airtravel_q#.csv
    
    Returns
    -------
    data frame
    '''
    
    qs = ['q1', 'q2', 'q3', 'q4']

    raw_ls = []
    for q in qs:
        raw = pd.read_csv(oj(data_dir, 'quarter_data', 'bts_airtravel_' + q + '.csv'))
        raw_ls.append(raw.iloc[:,:-1])
    raw = pd.concat(raw_ls)
    
    return raw

if __name__ == '__main__':
    raw = load_bts_airtravel()
    print('loaded bts_airtravel successfully.')

