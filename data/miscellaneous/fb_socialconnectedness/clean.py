#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os
import numpy as np
import argparse

if __name__ == '__main__':
    import sys
    sys.path.append(oj(os.path.dirname(__file__)))
    from load import load_fb_socialconnectedness
else:
    from .load import load_fb_socialconnectedness

def clean_fb_socialconnectedness(data_dir='.', level='county_county'):
    ''' Clean Facebook Social Connectedness Index Data (2020)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find cleaned csv
    level : str; one of 'country_country', 'county_country', 'county_county',
        'gadm1_nuts2', 'gadm1_nuts3'; specifies level of granularity of data
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    df = load_fb_socialconnectedness(data_dir = data_dir, level = level)
    
    # rename columns
    df = df.rename(columns = {"user_loc": "Location1", "fr_loc": "Location2", "scaled_sci": "SCI"})
    
    # county FIPS to string with padded zeros if applicable
    if level == 'county_county':
        df['Location1'] = df['Location1'].astype(int).astype(str).str.zfill(5)
        df['Location2'] = df['Location2'].astype(int).astype(str).str.zfill(5)
    elif level == 'county_country':
        df['Location1'] = df['Location1'].astype(int).astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(data_dir, "fb_socialconnectedness_" + level + ".csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', dest='level', action='store', 
                        default='county_county', help='level of granularity')
    args = parser.parse_args()
    df = clean_fb_socialconnectedness(level = args.level)
    print("cleaned fb_socialconnectedness successfully.")

