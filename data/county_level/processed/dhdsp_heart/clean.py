#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.dhdsp_heart.load import load_dhdsp_heart

def clean_dhdsp_heart(data_dir='../../raw/dhdsp_heart/', 
                        out_dir='.'):
    ''' Clean CDC DHDSP heart disease mortality data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_dhdsp_heart(data_dir = data_dir)
    
    # drop features
    drop_keys = ['display_name', 'theme_range']
    df = df.drop(columns = drop_keys)
    
    # rename features
    remap = {
        'cnty_fips': 'countyFIPS',
        'Value': 'HeartDiseaseMortality'
    }
    df = df.rename(columns = remap)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "dhdsp_heart.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_dhdsp_heart()
    print("cleaned dhdsp_heart successfully.")
