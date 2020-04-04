#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

import sys
sys.path.append('../../raw/brfss_smoking/')
from load import load_brfss_smoking

def clean_brfss_smoking(data_dir='../../raw/brfss_smoking/', 
                        out_dir='.'):
    ''' Clean BRFSS Adult Smoking data (2017)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_brfss_smoking(data_dir = data_dir)
    
    # rename features
    remap = {
        'FIPS': 'countyFIPS',
        '% Smokers': 'Smoking',
        '95% CI - Low.5': 'SmokingLowCI95',
        '95% CI - High.5': 'SmokingHighCI95'
    }
    
    df = df.rename(columns = remap)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "brfss_smoking.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_brfss_smoking()
    print("cleaned brfss_smoking successfully.")

