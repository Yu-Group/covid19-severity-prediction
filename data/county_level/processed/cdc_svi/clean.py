#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.cdc_svi.load import load_cdc_svi

def clean_cdc_svi(data_dir='../../raw/cdc_svi/', 
                  out_dir='.'):
    ''' Clean CDC Social Vulnerability Index data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_cdc_svi(data_dir = data_dir)
    
    # keep important variables
    df = df[['FIPS', 'RPL_THEMES', 'RPL_THEME1', 'RPL_THEME2',
             'RPL_THEME3', 'RPL_THEME4']]
    
    # rename features
    remap = {
        'FIPS': 'countyFIPS',
        'RPL_THEMES': 'SVIPercentile',
        'RPL_THEME1': 'SVIPercentileSEtheme',
        'RPL_THEME2': 'SVIPercentileHDtheme',
        'RPL_THEME3': 'SVIPercentileMLtheme',
        'RPL_THEME4': 'SVIPercentileHTtheme'
    }
    df = df.rename(columns = remap)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "cdc_svi.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_cdc_svi()
    print("cleaned cdc_svi successfully.")

