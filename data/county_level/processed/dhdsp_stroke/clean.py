#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.dhdsp_stroke.load import load_dhdsp_stroke

def clean_dhdsp_stroke(data_dir='../../raw/dhdsp_stroke/', 
                        out_dir='.'):
    ''' Clean CDC DHDSP stroke mortality data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_dhdsp_stroke(data_dir = data_dir)
    
    # drop features
    drop_keys = ['display_name', 'theme_range']
    df = df.drop(columns = drop_keys)
    
    # rename features
    remap = {
        'cnty_fips': 'countyFIPS',
        'Value': 'StrokeMortality'
    }
    df = df.rename(columns = remap)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "dhdsp_stroke.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_dhdsp_stroke()
    print("cleaned dhdsp_stroke successfully.")