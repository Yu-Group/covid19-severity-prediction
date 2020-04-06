#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.hpsa_shortage.load import load_hpsa_shortage

def clean_hpsa_shortage(data_dir='../../raw/hpsa_shortage/', 
                        out_dir='.'):
    ''' Clean Health Professional Shortage Areas (HPSA)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_hpsa_shortage(data_dir = data_dir)
    
    # filter data
    df = df[df['HPSA Component Type Description'] == 'Single County']
    df = df[df['HPSA Status'] == 'Designated']
    
    # rename features
    remap = {
        'State and County Federal Information Processing Standard Code': 'countyFIPS', 
        'State Name': 'State',
        'Common State Abbreviation': 'State Name',
        'County Equivalent Name': 'County Name',
        'Common County Name': 'Location',
        'HPSA Name': 'HPSAName',
        'HPSA Score': 'HPSAScore',
        'Metropolitan Indicator': 'HPSAMetroIndicator',
        '% of Population Below 100% Poverty': 'HPSAPercentPoverty',
        'Rural Status': 'HPSARuralStatus',
        'HPSA Estimated Served Population': 'HPSAServedPop',
        'HPSA Estimated Underserved Population': 'HPSAUnderservedPop',
        'HPSA Shortage': 'HPSAShortage'
    }
    df = df.rename(columns = remap)
    
    # keep important features
    df = df[['countyFIPS', 'State', 'State Name', 'County Name', 'Location', 
             'HPSAName', 'HPSAScore', 'HPSAMetroIndicator', 'HPSAPercentPoverty',
             'HPSARuralStatus', 'HPSAServedPop', 'HPSAUnderservedPop', 'HPSAShortage']]
    
    # write out to csv
    df.to_csv(oj(out_dir, "hpsa_shortage.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_hpsa_shortage()
    print("cleaned hpsa_shortage successfully.")