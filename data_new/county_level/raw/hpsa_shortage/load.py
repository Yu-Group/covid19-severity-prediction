#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_hpsa_shortage(data_dir='./'):
    ''' Load in Health Professional Shortage Areas (HPSA)
    
    Parameters
    ----------
    data_dir : str; path to the data directory with hpsa_shortage.csv
    
    Returns
    -------
    data frame
    '''
    
    raw = pd.read_excel(oj(data_dir, 'hpsa_shortage.xlsx'), 
                        sheet_name = "BCD_HPSA_FCT_DET")
    return raw


if __name__ == '__main__':
    raw = load_hpsa_shortage()
    print('loaded ahrf_health successfully.')

