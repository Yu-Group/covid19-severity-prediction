#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.khn_icu.load import load_khn_icu

def clean_khn_icu(data_dir='../../raw/khn_icu/', 
                  out_dir='.'):
    ''' Clean Kaiser Health News ICU Beds by County Data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_khn_icu(data_dir = data_dir)
    
    # drop features
    drop_keys = ["hospitals_in_cost_reports", "Total_pop", "60plus", "60plus_pct"]
    df = df.drop(columns = drop_keys)
    
    # rename features
    remap = {
        'cnty_fips': 'countyFIPS',
        'cnty_name': 'County Name',
        'st': 'State Name',
        'state': 'State',
        'Hospitals_in_HC': '#Hospitals',
        'all_icu': '#ICU_beds',
        '60plus_per_each_icu_bed': '60plusPerICUBed'
    }
    df = df.rename(columns = remap)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "khn_icu.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_khn_icu()
    print("cleaned khn_icu successfully.")

