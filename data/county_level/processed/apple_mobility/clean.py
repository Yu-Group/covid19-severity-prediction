#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

if __name__ == '__main__':
    import sys
    sys.path.append(oj(os.path.dirname(__file__), '../../raw/apple_mobility/'))
    from load import load_apple_mobility
else:
    from ...raw.apple_mobility.load import load_apple_mobility

def clean_apple_mobility(data_dir='../../raw/apple_mobility/', 
                         out_dir='.'):
    ''' Clean Apple Maps Mobility Trends data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    df = load_apple_mobility(data_dir)
    
    GOOD_COLS = {
        "geo_type": "Region Type",
        "region": "Region",
        "transportation_type": "Sector"
    }
    
    del df['alternative_name'] 
    
    df = pd.melt(df, id_vars=GOOD_COLS.keys(),
                 value_vars=set(df.columns) - set(GOOD_COLS.keys()), 
                 var_name='Date', value_name='Percent Change')
    
    df['Percent Change'] = df['Percent Change'] - 100.
    df = df.rename(columns=GOOD_COLS)
    
    # rename countries to match with google mobility
    df = df.replace({'Czech Republic': 'Czechia', 'Republic of Korea': 'South Korea', 'UK': 'United Kingdom'})
    
    # rename region types to match with google mobility
    df = df.replace({'country/region': 'Country', 'sub-region': 'State/Province', 'city': 'City'})
    
    df = df[["Region Type", "Region", "Date", "Sector", "Percent Change"]]
    df.to_csv(oj(out_dir, "apple_mobility.csv"), header=True, index=False)
    
    return df
    
    
if __name__ == '__main__':
    df = clean_apple_mobility()
    print("cleaned apple_mobility successfully.")