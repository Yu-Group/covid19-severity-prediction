#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_commute(data_dir='./'):
    ''' Load in county level Commute data (2011 - 2015)
    
    Parameters
    ----------
    data_dir : str; path to the data directory with table[numbers 1 to 4].xlsx
    
    Returns
    -------
    data frame
    '''
    
    # load in the table sorted by resident county, remove header and footer
    raw = pd.read_excel(oj(data_dir, 'table1.xlsx'), header=6, dtype=str)
    raw = raw.iloc[:-2, :]

    return raw


if __name__ == '__main__':
    raw = load_commute()
    print('loaded table1.xlsx successfully.')
    