#! /usr/bin/python3

import pandas as pd
import numpy as np
from os.path import join as oj
import os
from tqdm import tqdm

from ...raw.mit_voting.load import load_mit_voting

def clean_mit_voting(data_dir='../../raw/mit_voting/', 
                     out_dir='.'):
    ''' Clean 2000-2016 County Presidential Data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_mit_voting(data_dir = data_dir)
    
    # only keep data from republican and democratic parties in 2016 election
    df = df[df['year'] == 2016]
    df = df[(df['party'] == 'democrat') | (df['party'] == 'republican')]
    df = df[~df.FIPS.isna()]
    df['FIPS'] = df.FIPS.astype(int)
    
    # compute additional statistic: democrat-to-republican ratio
    ks = sorted(np.unique(df.FIPS))
    r = {'countyFIPS': ks, 
         'dem_to_rep_ratio': []}
    for k in tqdm(ks):
        v = df[df.FIPS == k]
        ratio = v[v.party == 'democrat'].candidatevotes.iloc[0] / v[v.party == 'republican'].candidatevotes.iloc[0]
        r['dem_to_rep_ratio'].append(ratio)
    df = pd.DataFrame.from_dict(r)
    
    # county FIPS to string with padded zeros
    df['countyFIPS'] = df['countyFIPS'].astype(int).astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "mit_voting.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_mit_voting()
    print("cleaned mit_voting successfully.")
