#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

if __name__ == '__main__':
    import sys
    sys.path.append(oj(os.path.dirname(__file__), '..', '..', 'raw', 'ccd_daily'))
    from load import load_ccd_daily
else:
    from ...raw.ccd_daily.load import load_ccd_daily


def clean_ccd_daily(data_dir=oj('..', '..', 'raw', 'ccd_daily'),
                    out_dir='.'):
    ''' Clean Covid County Data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_ccd_daily(data_dir = data_dir)
    
    # rename features
    remap = {
        'dt': 'Date',
        'county_fips': 'countyFIPS',
        'county_name': 'County'
    }
    df = df.rename(columns = remap)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    # convert date to datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # write out to csv
    df.to_csv(oj(out_dir, "ccd_daily.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_ccd_daily()
    print("cleaned ccd_daily successfully.")

