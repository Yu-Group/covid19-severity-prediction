#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os


def load_usda_poverty(data_dir ='./'):
    ''' Load in USDA Poverty Data 2018
    
    Parameters
    ----------
    data_dir : str; path to the data directory with Poverty_data.xls
    
    Returns
    -------
    data frame
    '''

    raw = pd.read_excel(oj(data_dir, 'usda_poverty.xls'), 
                        sheet_name="Poverty Data 2018", skiprows=4)
    return raw


if __name__ == '__main__':
    raw = load_usda_poverty()
    print('loaded usda_poverty successfully.')

