#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_streetlight_vmt(data_dir='../../../../../covid-19-private-data'):
    ''' Load in Streetlight Vehicle Miles Traveled
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw streetlight_vmt.csv
    
    Returns
    -------
    data frame
    '''
    
    orig_dir = os.getcwd()
    os.chdir(data_dir)

    # refresh and load in data
    os.system("git pull")
    raw = pd.read_csv("streetlight_vmt.csv")
    
    os.chdir(orig_dir)
    
    return raw

if __name__ == '__main__':
    raw = load_streetlight_vmt()
    print('loaded streetlight_vmt successfully.')


