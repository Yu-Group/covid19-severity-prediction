#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_fb_socialconnectedness(data_dir='.', level='county_county'):
    ''' Load in Facebook Social Connectedness Index Data (2020)
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing raw data
    level : str; one of 'country_country', 'county_country', 'county_county',
        'gadm1_nuts2', 'gadm1_nuts3'; specifies level of granularity of data
    
    Returns
    -------
    data frame in long format
    '''
    
    if level == 'country_country':
        fn = 'country_country_aug2020.tsv'
    elif level == 'county_country':
        fn = 'county_country_aug2020.tsv'
    elif level == 'county_county':
        fn = 'county_county_aug2020.tsv'
    elif level == 'gadm1_nuts2':
        fn = 'gadm1_nuts2_gadm1_nuts2_aug2020.tsv'
    elif level == 'gadm1_nuts3':
        fn = 'gadm1_nuts3_counties_gadm1_nuts3_counties_Aug2020.tsv'
    else:
        raise ValueError("level is unknown.")

    raw = pd.read_csv(oj(data_dir, fn), sep = '\t')
    
    return raw

if __name__ == '__main__':
    raw = load_fb_socialconnectedness()
    print('loaded fb_socialconnectedness successfully.')

