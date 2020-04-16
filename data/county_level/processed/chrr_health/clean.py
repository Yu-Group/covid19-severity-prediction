#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.chrr_health.load import load_chrr_health

def clean_chrr_health(data_dir='../../raw/chrr_health/', 
                      out_dir='.'):
    ''' Clean County Health Rankings & Roadmaps data (2020)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_chrr_health(data_dir = data_dir)
    
    # rename features
    remap = {
        'FIPS': 'countyFIPS',
        '% Smokers': 'Smokers_Percentage'
    }
    
    # convert ratios (strings) to fractions
    df = df.rename(columns = remap)
    for ratio in ["Primary Care Physicians Ratio", "Dentist Ratio", 
                  "Mental Health Provider Ratio"]:
        df[ratio] = df[ratio].str.split(":", expand=True).iloc[:, 0].astype(float) / df[ratio].str.split(":", expand=True).iloc[:, 1].astype(float)
    
    # convert string to binary
    df["Presence of Water Violation"] = df["Presence of Water Violation"].map(dict(Yes=1, No=0))
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "chrr_health.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_chrr_health()
    print("cleaned chrr_health successfully.")

