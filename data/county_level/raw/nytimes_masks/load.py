#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_nytimes_masks(data_dir='.'):
    ''' Load in the New York Times and Dynata Mask-Wearing Survey data set (pulled directly from GitHub source)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to write raw nytimes_masks.csv
    
    Returns
    -------
    data frame
    '''
    
    raw = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/mask-use/mask-use-by-county.csv")
    raw.to_csv(oj(data_dir, "nytimes_masks.csv"), header=True, index=False)

    return raw

if __name__ == '__main__':
    raw = load_nytimes_mask()
    print('loaded nytimes_mask successfully.')



