#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.usdss_diabetes.load import load_usdss_diabetes

def clean_usdss_diabetes(data_dir='../../raw/usdss_diabetes/',
                         out_dir='.'):
    ''' Clean USDSS Diagnosed Diabetes data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_usdss_diabetes(data_dir = data_dir)
    
    # rename features
    remap = {
        'CountyFIPS': 'countyFIPS',
        'Percentage': 'DiabetesPercentage',
        'Lower Limit': 'DiabetesLowCI95',
        ' Upper Limit': 'DiabetesHighCI95'
    }
    df = df.rename(columns = remap)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(int).astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "usdss_diabetes.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_usdss_diabetes()
    print("cleaned usdss_diabetes successfully.")