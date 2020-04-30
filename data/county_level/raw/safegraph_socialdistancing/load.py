#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_safegraph_socialdistancing(data_dir='../../../../../covid-19-private-data'):
    ''' Load in SafeGraph Social Distancing data (automatically updated)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find safegraph_socialdistancing.gz (private data)
    
    Returns
    -------
    data frame
    '''
    
    orig_dir = os.getcwd()
    os.chdir(data_dir)

    # refresh and load in data
    os.system("git pull")
    raw = pd.read_pickle("safegraph_socialdistancing.gz", compression="gzip")
    
    os.chdir(orig_dir)
    
    return raw

if __name__ == '__main__':
    raw = load_safegraph_socialdistancing()
    print('loaded safegraph_socialdistancing successfully.')


