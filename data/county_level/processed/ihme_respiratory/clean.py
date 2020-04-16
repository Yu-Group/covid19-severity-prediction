#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.ihme_respiratory.load import load_ihme_respiratory

def clean_ihme_respiratory(data_dir='../../raw/ihme_respiratory/', 
                           out_dir='.'):
    ''' Clean US Chronic Respiratory Disease Mortality Data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_ihme_respiratory(data_dir = data_dir)
    
    # rename features
    remap = {
        'FIPS': 'countyFIPS',
        'Mortality Rate, 1980*': 'RespMortalityRate1980',
        'Mortality Rate, 1985*': 'RespMortalityRate1985',
        'Mortality Rate, 1990*': 'RespMortalityRate1990',
        'Mortality Rate, 1995*': 'RespMortalityRate1995',
        'Mortality Rate, 2000*': 'RespMortalityRate2000',
        'Mortality Rate, 2005*': 'RespMortalityRate2005',
        'Mortality Rate, 2010*': 'RespMortalityRate2010',
        'Mortality Rate, 2014*': 'RespMortalityRate2014',
        '% Change in Mortality Rate, 1980-2014': 'ChangeInRespMortality1980-2014'
    }
    df = df.rename(columns = remap)
    
    # split estimates and CI into separate columns
    for col in list(df.columns)[2:]:
        colnames = [col, col + 'LowCI95', col + 'HighCI95']
        df[colnames] = df[colnames[0]].str.split(expand = True)
        df[colnames[0]] = df[colnames[0]].astype(float)
        df[colnames[1]] = df[colnames[1]].str.replace("\(|,", "").astype(float)
        df[colnames[2]] = df[colnames[2]].str.replace('\)', "").astype(float)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(int).astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "ihme_respiratory.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_ihme_respiratory()
    print("cleaned ihme_respiratory successfully.")