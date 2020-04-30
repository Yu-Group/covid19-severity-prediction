#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.unacast_mobility.load import load_unacast_mobility

def clean_unacast_mobility(data_dir='../../../../../covid-19-private-data',
                           out_dir='.'):
    ''' Clean Unacast Social Mobility and Distancing data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_unacast_mobility(data_dir = data_dir)
    
    # drop features
    drop_keys = ['weekday', 'covid', 'state_fips', 'county_population', 
                 'grade_total', 'grade_distance', 'grade_visitation', 
                 'n_grade_total', 'n_grade_distance', 'n_grade_visitation',
                 'grade_encounters', 'n_grade_encounters', 'last_updated']
    df = df.drop(columns = drop_keys)
    
    # rename features
    remap = {
        'county_fips': 'countyFIPS', 
        'state_name': 'State',
        'state_code': 'State Name',
        'county_name': 'County'
    }
    df = df.rename(columns = remap)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    # convert to wide format
    df = df.pivot(index = 'countyFIPS', columns = 'date', 
                  values = ['daily_distance_diff', 'daily_visitation_diff',
                            'encounters_rate'])
    df = pd.DataFrame(df.to_records())
    df.columns = [col.replace("('", "").replace("', '", "").replace("')", "") \
                  for col in df.columns]
    
    # write out to csv
    df.to_csv(oj(out_dir, "unacast_mobility.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_unacast_mobility()
    print("cleaned unacast_mobility successfully.")
