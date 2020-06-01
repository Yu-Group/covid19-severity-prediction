#! /usr/bin/python3

import pandas as pd
import os
from os.path import join as oj
import numpy as np

from load import load_commute

def clean_commute(data_dir='./', 
                      out_dir='./'):
    ''' Clean commute database (2011-2015, sorted by resident location)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_commute(data_dir)

    # rename columns
    df.columns = [
        'Resident State FIPS',
        'Resident County FIPS',
        'Resident State Name',
        'Resident County Name',
        'Work State FIPS',
        'Work County FIPS',
        'Work State Name',
        'Work County Name',
        'commute',
        'error',
    ]

    # change commute data types
    df['commute'] = df['commute'].astype(np.float)
    df['error'] = df['error'].astype(np.float)

    # formatting FIPS
    df['Work State FIPS'] = df['Work State FIPS'].apply(lambda x : x[1:] if type(x) == str else np.nan)
    df['Resident County FIPS'] = df['Resident State FIPS'] + df['Resident County FIPS']
    df['Work County FIPS'] = df['Work State FIPS'] + df['Work County FIPS']

    # drop work place with no FIPS (places outside of the US)
    df = df.dropna(subset=['Work County FIPS'])

    # drop the two resident counties that are not listed in the reference file with
    # FIPS: 02158 and 46102, both counties have small number of commuters with large error
    df = df[~df['Resident County FIPS'].isin(['02158', '46102'])]

    # drop columns that are not needed
    df = df.drop(['Resident State FIPS', 'Resident State Name', 'Resident County Name', 'Work State FIPS', 'Work State Name', 'Work County Name'], axis=1)

    # write the cleaned table to csv
    df.to_csv(oj(out_dir, 'commute.csv'), header=True, index=False)

    return df

if __name__ == '__main__':
    df = clean_commute()
    print("cleaned commute successfully.")
