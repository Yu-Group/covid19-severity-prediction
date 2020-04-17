#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.jhu_interventions.load import load_jhu_interventions

def clean_jhu_interventions(data_dir='../../raw/jhu_interventions/', 
                            out_dir='.'):
    ''' Clean JHU Interventions (county-level) data set (pulled directly from GitHub source)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_jhu_interventions(data_dir = data_dir)
    
    # rename features
    remap = {
        'FIPS': 'countyFIPS',
        'AREA_NAME': 'County Name',
        'STATE': 'State Name'
    }
    df = df.rename(columns = remap)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "jhu_interventions.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_jhu_interventions()
    print("cleaned jhu_interventions successfully.")

