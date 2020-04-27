#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.safegraph_socialdistancing.load import load_safegraph_socialdistancing

def clean_safegraph_socialdistancing(data_dir='../../../../../covid-19-private-data',
                                     out_dir='.'):
    ''' Clean SafeGraph Social Distancing data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find load function
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_safegraph_socialdistancing(data_dir = data_dir)
    
    # convert to wide format
    cols = [col for col in df.columns.tolist() if not col in ['countyFIPS', 'date']]
    df = df.pivot(index = 'countyFIPS', columns = 'date', values = cols)
    df = pd.DataFrame(df.to_records())
    df.columns = [col.replace("('", "").replace("', '", "_").replace("')", "") \
                  for col in df.columns]
    
	# write out to pickle (large file)
    #df.to_pickle(oj(out_dir, "safegraph_socialdistancing.gz"), compression="gzip")

    return df

if __name__ == '__main__':
    df = clean_safegraph_socialdistancing()
    print("cleaned safegraph_socialdistancing successfully.")
