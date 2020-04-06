#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.chrr_smoking.load import load_chrr_smoking

def clean_chrr_smoking(data_dir='../../raw/chrr_smoking/', 
                       out_dir='.'):
    ''' Clean County Health Rankings & Roadmaps Adult Smoking data (2017)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_chrr_smoking(data_dir = data_dir)
    
    # rename features
    remap = {
        'FIPS': 'countyFIPS',
        '% Smokers': 'Smokers_Percentage',
        '95% CI - Low.5': 'SmokersLowCI95',
        '95% CI - High.5': 'SmokersHighCI95'
    }
    
    df = df.rename(columns = remap)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "chrr_smoking.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_chrr_smoking()
    print("cleaned chrr_smoking successfully.")

