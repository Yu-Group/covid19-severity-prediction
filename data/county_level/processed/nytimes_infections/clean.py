#! /usr/bin/python3

import pandas as pd
import os
from os.path import join as oj
from os.path import dirname

if __name__ == '__main__':
    import sys
    sys.path.append(oj(os.path.dirname(__file__), '../../raw/nytimes_infections/'))
    from load import load_nytimes_infections
else:
    from ...raw.nytimes_infections.load import load_nytimes_infections


def clean_nytimes_infections(data_dir='../../raw/nytimes_infections/', 
                      out_dir='.'):
    ''' Clean nytimes data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_nytimes_infections(data_dir = data_dir)
    
    # write out to csv
    df.to_csv(oj(out_dir, "nytimes_infections.csv"), index=False)
    
    return df

if __name__ == '__main__':
    df = clean_nytimes_infections()
    print("cleaned nytimes infections successfully.")

