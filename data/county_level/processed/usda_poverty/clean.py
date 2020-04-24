#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
from os.path import dirname
import os




if __name__ == '__main__':
    import sys
    sys.path.append(oj(os.path.dirname(__file__), '../../raw/usda_poverty'))
    from load import load_usda_poverty
else:
    from ...raw.usda_poverty.load import load_usda_poverty


def clean_usda_poverty(data_dir='../../raw/usda_poverty/', 
                      out_dir='.'):
    ''' Clean US Dept of Agriculture Poverty Data 2018
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_usda_poverty(data_dir = data_dir)
    # drop features
    drop_keys = ['Rural-urban_Continuum_Code_2003','Urban_Influence_Code_2003', 
                 'Rural-urban_Continuum_Code_2013', 'CI90LBAll_2018',
                 'CI90UBALL_2018','CI90LBALLP_2018','CI90UBALLP_2018',		
                 'CI90LB017_2018','CI90UB017_2018','CI90LB017P_2018',
                 'CI90UB017P_2018','CI90LB517_2018','CI90UB517_2018',
                 'CI90LB517P_2018', 'CI90UB517P_2018', 'CI90LBINC_2018',
                 'CI90UBINC_2018','POV04_2018','CI90LB04_2018', 'CI90UB04_2018',
                 'PCTPOV04_2018','CI90LB04P_2018','CI90UB04P_2018']


  
    df = df.drop(columns = drop_keys)
    
    # rename features
    remap = {'FIPStxt': 'countyFIPS', 'Stabr': 'State', 'Area_name':'County',	
             'Urban_Influence_Code_2013':'Urban Influence Code 2013',
             'POVALL_2018': 'Poverty Num All Ages 2018',
             'PCTPOVALL_2018': 'Poverty Pct All Ages 2018',
             'POV017_2018': 'Poverty Num Ages 0-17 2018',
             'PCTPOV017_2018': 'Poverty Pct Ages 0-17 2018',
             'POV517_2018': 'Poverty Num Ages 5-17 2018',
             'PCTPOV517_2018': 'Poverty Pct Ages 5-17 2018',
             'MEDHHINC_2018': 'Median Household Income 2018'}

 
    df = df.rename(columns = remap)
    df=df.dropna(axis=0, subset=['Urban Influence Code 2013'])

    df["countyFIPS"] = df["countyFIPS"].astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "usda_poverty.csv"), header=True, index=False)
    
    return df


if __name__ == '__main__':
    df = clean_usda_poverty()
    print("cleaned usda poverty successfully.")

