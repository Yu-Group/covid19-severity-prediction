#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

if __name__ == '__main__':
    import sys
    sys.path.append(oj(os.path.dirname(__file__), "..", "..", "raw", "nytimes_masks"))
    from load import load_nytimes_masks
else:
    from ...raw.nytimes_masks.load import load_nytimes_masks
    

def clean_nytimes_masks(data_dir=oj("..", "..", "raw", "nytimes_masks"),
                        out_dir='.'):
    ''' Clean New York Times and Dynata Mask-Wearing Survey data set (pulled directly from GitHub source)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_nytimes_masks(data_dir = data_dir)
    
    # rename features
    remap = {
        'COUNTYFP': 'countyFIPS',
        'NEVER': 'Mask Never',
        'RARELY': 'Mask Rarely',
        'SOMETIMES': 'Mask Sometimes',
        'FREQUENTLY': 'Mask Frequently',
        'ALWAYS': 'Mask Always',
    }
    df = df.rename(columns = remap)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "nytimes_masks.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_nytimes_masks()
    print("cleaned nytimes_masks successfully.")



