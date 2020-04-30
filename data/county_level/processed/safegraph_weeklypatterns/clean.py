#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

from ...raw.safegraph_weeklypatterns.load import load_safegraph_weeklypatterns

def clean_safegraph_weeklypatterns(data_dir='../../../../../covid-19-private-data',
                                   out_dir='.', grouping='specialty'):
    ''' Clean SafeGraph Weekly Patterns data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find load function
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_safegraph_weeklypatterns(data_dir = data_dir, grouping=grouping)
        
    # convert to wide format
    cols = [col for col in df.columns.tolist() if not col in ['countyFIPS', 'category']]
    df = df.pivot(index = 'countyFIPS', columns = 'category', values = cols)
    df = pd.DataFrame(df.to_records())
    df.columns = [col.replace("('", "").replace("', '", "_").replace("')", "") \
                  for col in df.columns]
    
	# write out to pickle (large file)
    #df.to_pickle(oj(out_dir, "safegraph_weeklypatterns.gz"), compression="gzip")

    return df

if __name__ == '__main__':
    df = clean_safegraph_weeklypatterns()
    print("cleaned safegraph_weeklypatterns successfully.")
