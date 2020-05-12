#! /usr/bin/python3

import pandas as pd
import numpy as np
import os
from os.path import join as oj
from os.path import dirname

if __name__ == '__main__':
    import sys
    sys.path.append(oj(os.path.dirname(__file__), '../../raw/usafacts_infections/'))
    from load import load_usafacts_infections
else:
    from ...raw.usafacts_infections.load import load_usafacts_infections


def clean_usafacts_infections(data_dir='../../raw/usafacts_infections/', 
                      out_dir='.'):
    ''' Clean usafacts data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_usafacts_infections(data_dir = data_dir)

    # two counties changed their county FIPS
    if "02158" in df["countyFIPS"].unique():
        df.loc[df["countyFIPS"] == "02158", "countyFIPS"] = "02270"
    if "46102" in df["countyFIPS"].unique():
        df.loc[df["countyFIPS"] == "46102", "countyFIPS"] = "46113"
    # merge counties countyFIPS")with the same countyFIPS
    df = df.groupby("countyFIPS").sum().reset_index()

    # remove princess cruise ship
    df = df[df['countyFIPS'] != "06000"]

    # write out to csv
    df.to_csv(oj(out_dir, "usafacts_infections.csv"), index=False)
    
    return df

if __name__ == '__main__':
    df = clean_usafacts_infections()
    print("cleaned usafacts infections successfully.")

