#!/usr/bin/python3

import numpy as np
import pandas as pd
import os
from os.path import join as oj
import sys

from ...raw.nyt_nursinghomes.load import load_nyt_nursinghomes
    

def clean_nyt_nursinghomes(data_dir='../../raw/nyt_nursinghomes/', 
                           out_dir = "."):
    ''' Clean NYT Nursing Home COVID-19 data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    data frame
    '''

    # load in data
    df = load_nyt_nursinghomes(data_dir = data_dir)
    
    # reorder columns
    cols = ["Name", "City", "State"] +\
                [col for col in list(df.columns) if col not in ["Name", "City", "State"]]
    df = df[cols]
    
    # write out to csv
    df.to_csv(oj(out_dir, "nyt_nursinghomes.csv"), header=True, index=False)
    return df


if __name__ == '__main__':
    df = clean_nyt_nursinghomes()
    print("cleaned nyt_nursinghomes successfully.")

