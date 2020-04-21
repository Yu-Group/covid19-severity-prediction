#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.kinsa_ili.load import load_kinsa_ili

def clean_kinsa_ili(data_dir='../../../../../covid-19-private-data', 
                    out_dir='.'):
    ''' Clean Kinsa Influenza-like Illness weather map data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_kinsa_ili(data_dir = data_dir)
    
    # drop features and duplicates
    df = df.drop_duplicates()
    drop_keys = ['doy']
    df = df.drop(columns = drop_keys)
    
    # rename features
    remap = {
        'region_id': 'countyFIPS', 
        'region_name': 'County',
        'state': 'State Name',
        'county_name': 'County'
    }
    df = df.rename(columns = remap)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    # drop duplicates
    df = df.drop_duplicates(subset=['countyFIPS', 'date'], keep='first')
    
    # convert to wide format
    df = df.pivot(index = 'countyFIPS', columns = 'date', 
                  values = ['observed_ili', 'atypical_ili', 'anomaly_diff', 
                            'forecast_expected', 'forecast_lower', 'forecast_upper'])
    df = pd.DataFrame(df.to_records())
    df.columns = [col.replace("('", "").replace("', '", "").replace("')", "") \
                  for col in df.columns]
    
    # write out to csv
    df.to_csv(oj(out_dir, "kinsa_ili.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_kinsa_ili()
    print('cleaned kinsa_ili successfully.')

