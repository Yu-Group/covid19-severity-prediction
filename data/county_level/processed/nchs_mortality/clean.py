#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.nchs_mortality.load import load_nchs_mortality

def clean_nchs_mortality(data_dir='../../raw/nchs_mortality/',
                         out_dir='.'):
    ''' Clean NCHS Compressed Mortality Data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_nchs_mortality(data_dir = data_dir)
    
    # rename features
    remap = {
        'County Code': 'countyFIPS',
        'Crude Rate': 'CrudeMortalityRate2012-2016'
    }
    df = df.rename(columns = remap)
    
    # verify/recompute crude mortality rate
    df['CrudeMortalityRate2012-2016'] = df.Deaths / df.Population * 100000
    
    # drop features
    drop_keys = ['Notes', 'County', 'Deaths', 'Population']
    df = df.drop(columns = drop_keys)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(int).astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "nchs_mortality.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_nchs_mortality()
    print("cleaned nchs_mortality successfully.")
