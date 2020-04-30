#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_safegraph_weeklypatterns(data_dir='../../../../../covid-19-private-data', 
                                  grouping='specialty'):
    ''' Load in SafeGraph Weekly Patterns data (automatically updated)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find safegraph_weeklypatterns*.gz (private data)
    
    grouping : either 'main' or 'specialty'; specifies which industry grouping schema to use
    
    Returns
    -------
    data frame
    '''
    
    orig_dir = os.getcwd()
    os.chdir(data_dir)

    # refresh and load in data
    os.system("git pull")
    if grouping == 'main':
        raw = pd.read_pickle("safegraph_weeklypatterns_grouped1.gz", compression="gzip")
    elif grouping == 'specialty':
        raw = pd.read_pickle("safegraph_weeklypatterns_grouped2.gz", compression="gzip")
    else:
        raise ValueError("grouping must be either 'main' or 'specialty'")
    
    os.chdir(orig_dir)
    
    return raw

if __name__ == '__main__':
    raw = load_safegraph_weeklypatterns()
    print('loaded safegraph_weeklypatterns successfully.')


