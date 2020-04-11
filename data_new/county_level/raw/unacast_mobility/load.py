#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_unacast_mobility(data_dir='../../../../../covid-19-private-data'):
    ''' Load in Unacast Social Mobility and Distancing data (automatically updated)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw unacast_mobility.csv
    
    Returns
    -------
    data frame
    '''
    
    orig_dir = os.getcwd()
    os.chdir(data_dir)

    # refresh and load in data
    os.system("git pull")
    raw = pd.read_csv("unacast_mobility.csv")
    
    os.chdir(orig_dir)
    
    return raw

if __name__ == '__main__':
    raw = load_unacast_mobility()
    print('loaded unacast_mobility successfully.')


