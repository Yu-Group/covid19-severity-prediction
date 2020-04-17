#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_dhdsp_stroke(data_dir='.'):
    ''' Load in CDC DHDSP stroke mortality data
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing dhdsp_stroke.csv
    
    Returns
    -------
    data frame
    '''
    
    # load in data
    raw = pd.read_csv(oj(data_dir, "dhdsp_stroke.csv"), 
                      na_values = [-1, -9999, ""])
    return raw

if __name__ == '__main__':
    raw = load_dhdsp_stroke()
    print('loaded dhdsp_stroke successfully.')

