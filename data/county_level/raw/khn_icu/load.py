#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_khn_icu(data_dir='.'):
    ''' Load in Kaiser Health News ICU Beds by County Data
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing khn_icu.xlsx
    
    Returns
    -------
    data frame
    '''
    
    raw = pd.read_excel(oj(data_dir, "khn_icu.xlsx"), sheet_name = "DATA")
    
    return raw

if __name__ == '__main__':
    raw = load_khn_icu()
    print('loaded khn_icu successfully.')



