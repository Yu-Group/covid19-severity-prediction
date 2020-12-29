#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

if __name__ == '__main__':
    import sys
    sys.path.append(oj(os.path.dirname(__file__), '..', '..', 'raw', 'dhhs_hospitalcapacity'))
    from load import load_dhhs_hospitalcapacity
else:
    from ...raw.dhhs_hospitalcapacity.load import load_dhhs_hospitalcapacity


def clean_dhhs_hospitalcapacity(data_dir=oj('..', '..', 'raw', 'dhhs_hospitalcapacity'),
                                out_dir='.'):
    ''' Clean Dept of Health and Human Services COVID-19 Reported Patient 
    Impact and Hospital Capacity by Facility
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_dhhs_hospitalcapacity(data_dir = data_dir)
    
    # rename features
    remap = {
        'collection_week': 'Week',
        'state': 'State',
        'ccn': 'CCN',
        'fips_code': 'countyFIPS'
    }
    df = df.rename(columns = remap)
    
    # county FIPS to string with padded zeros
    na_idx = df['countyFIPS'].isna()
    df.loc[~na_idx, 'countyFIPS'] = df.loc[~na_idx, 'countyFIPS'].astype(int).astype(str).str.zfill(5)
    
    # zip to string with padded zeros
    na_idx = df['zip'].isna()
    df.loc[~na_idx, 'zip'] = df.loc[~na_idx, 'zip'].astype(int).astype(str).str.zfill(5)
    
    # convert week to datetime format
    df['Week'] = pd.to_datetime(df['Week'])
    
    # write out to csv
    df.to_csv(oj(out_dir, "dhhs_hospitalcapacity.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_dhhs_hospitalcapacity()
    print("cleaned dhhs_hospitalcapcity successfully.")

