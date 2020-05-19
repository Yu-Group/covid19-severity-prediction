#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_google_mobility(data_dir='.'):
    ''' Load in Google Community Mobility Reports
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing 'google_mobility.csv'
    
    Returns
    -------
    data frame
    '''

    # download directly from source to get daily updates
    cur_dir = os.getcwd()
    os.chdir(data_dir)
    os.system("wget https://www.gstatic.com/covid19/mobility/Global_Mobility_Report.csv -O google_mobility.csv")
    raw = pd.read_csv('google_mobility.csv')
    os.chdir(cur_dir)
    
    return raw

if __name__ == '__main__':
    raw = load_google_mobility()
    print('loaded google_mobility successfully.')



