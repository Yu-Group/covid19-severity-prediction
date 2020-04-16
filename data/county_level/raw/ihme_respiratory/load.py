#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_ihme_respiratory(data_dir='.'):
    ''' Load in US Chronic Respiratory Disease Mortality Rates (1980-2014)
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing ihme_respiratory.xlsx
    
    Returns
    -------
    data frame
    '''
    
    raw = pd.read_excel(oj(data_dir, "ihme_respiratory.xlsx"), 
                        sheet_name = "Chronic respiratory diseases", 
                        skiprows = 1)
    raw = raw.dropna(subset = ['FIPS'])
    
    return raw

if __name__ == '__main__':
    raw = load_ihme_respiratory()
    print('loaded ihme_respiratory successfully.')



