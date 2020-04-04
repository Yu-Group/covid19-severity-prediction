#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_nchs_mortality(data_dir='.'):
    ''' Load in NCHS Compressed Mortality Data
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing 'nchs_mortality.txt'
    
    Returns
    -------
    data frame
    '''

    raw = pd.read_table(oj(data_dir, 'nchs_mortality.txt'), 
                           na_values = ["Suppressed", "Missing"])
    raw = raw.dropna(subset = ['County'])
    
    return raw

if __name__ == '__main__':
    raw = load_nchs_mortality()
    print('loaded nchs_mortality successfully.')



