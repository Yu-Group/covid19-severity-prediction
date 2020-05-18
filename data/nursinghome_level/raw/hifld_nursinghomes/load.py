#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_hifld_nursinghomes(data_dir='.'):
    ''' Load in HIFLD Nursing Homes Data (2019)
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing 
               ./hifld_nursinghomes_raw.csv
    
    Returns
    -------
    data frame
    '''
    
    raw = pd.read_csv(oj(data_dir, 'hifld_nursinghomes.csv'), 
                      na_values = [-999, "NOT AVAILABLE"])
    
    return raw

if __name__ == '__main__':
    raw = load_hifld_nursinghomes()
    print('loaded hifld_nursinghomes successfully.')

