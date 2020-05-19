#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os
from urllib.request import urlopen
from json import load

def load_apple_mobility(data_dir='.'):
    ''' Load in Apple Maps Mobility Trends
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing 'apple_mobility.csv'
    
    Returns
    -------
    data frame
    '''
    
    cur_dir = os.getcwd()
    os.chdir(data_dir)

    # Link updates every day and seems volatile (the current link is
    # https://covid19-static.cdn-apple.com/covid19-mobility-data/2008HotfixDev26/v2/en-us/applemobilitytrends-2020-05-13.csv
    # so we go through some extra steps to download from the right url
    BASE_PATH = "https://covid19-static.cdn-apple.com/"
    response = load(urlopen("https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v2/index.json"))
    CSV_PATH = BASE_PATH + response['basePath'] + response['regions']['en-us']['csvPath']
    os.system(f"wget {CSV_PATH} -O apple_mobility.csv")

    raw = pd.read_csv('apple_mobility.csv')
    os.chdir(cur_dir)
    
    return raw

if __name__ == '__main__':
    raw = load_apple_mobility()
    print('loaded apple_mobility successfully.')



