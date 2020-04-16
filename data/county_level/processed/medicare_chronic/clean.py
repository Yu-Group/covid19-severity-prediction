#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.medicare_chronic.load import load_medicare_chronic

def clean_medicare_chronic(data_dir='../../raw/medicare_chronic/', 
                           out_dir='.'):
    ''' Clean CMS Chronic Conditions Data (2017)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_medicare_chronic(data_dir = data_dir)
    
    # county FIPS to string with padded zeros
    df = df.dropna(subset = ['countyFIPS'])
    df['countyFIPS'] = df['countyFIPS'].astype(int).astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "medicare_chronic.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_medicare_chronic()
    print("cleaned medicare_chronic successfully.")