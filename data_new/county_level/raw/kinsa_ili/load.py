#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_kinsa_ili(data_dir='../../../../../covid-19-private-data'):
    ''' Load in Kinsa Influenza-like Illness weather map data (automatically updated)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw kinsa_ili.csv
    
    Returns
    -------
    data frame
    '''
    
    orig_dir = os.getcwd()
    os.chdir(data_dir)

    # refresh and load in data
    os.system("git pull")
    raw = pd.read_csv("kinsa_ili.csv")
    
    os.chdir(orig_dir)
    
    return raw

if __name__ == '__main__':
    raw = load_kinsa_ili()
    print('loaded kinsa_ili successfully.')

