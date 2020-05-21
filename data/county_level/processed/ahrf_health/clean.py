#! /usr/bin/python3

import pandas as pd
import os
from os.path import join as oj
from os.path import dirname

if __name__ == "__main__":
    import sys
    sys.path.append("../../raw/ahrf_health/")
    from load import load_ahrf_health
else:
    from ...raw.ahrf_health.load import load_ahrf_health

def clean_ahrf_health(data_dir='../../raw/ahrf_health/', 
                      out_dir='.'):
    ''' Clean Area Health Resources Files (2018-2019 Release)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_ahrf_health(data_dir = data_dir)
    
    # drop features
    drop_keys = ['Blank', 'EntityofFile', 'SecondaryEntityOfFile', 'DateofFile', 
                 'DateofCreation', 'FileLength', 'CountyNamew/StateAbbrev', 
                 'FIPSStateCode', 'FIPSCountyCode']
    df = df.drop(columns = drop_keys)
    
    # rename features
    remap = {
        'Header-FIPSStandCtyCode': 'countyFIPS',
        'StateName': 'State',
        'StateNameAbbreviation': 'State Name',
        'CountyName': 'County Name'
    }
    df = df.rename(columns = remap)

    df["countyFIPS"] = df["countyFIPS"].astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "ahrf_health.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_ahrf_health()
    print("cleaned ahrf_health successfully.")

