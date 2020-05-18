#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os
import numpy as np
import requests
import urllib

from ...raw.hifld_nursinghomes.load import load_hifld_nursinghomes


def clean_hifld_nursinghomes(data_dir='../../raw/hifld_nursinghomes/', 
                             out_dir='.'):
    ''' Clean HIFLD Nursing Homes Data (2019)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the output directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_hifld_nursinghomes(data_dir)
    
    # drop those with all nas
    #df = df.dropna(subset = ["POPULATION", "TOT_RES", "TOT_STAFF", "BEDS", "EXCESS_BED"],
    #               how = "all")
    
    # drop facilites that are closed
    df = df.loc[df["STATUS"] != "CLOSED"]
    
    # drop duplicates
    keys = ["NAME", "ADDRESS", "CITY", "STATE", "ZIP", "TYPE", "POPULATION",
            "COUNTYFIPS", "TOT_RES", "TOT_STAFF", "BEDS", "EXCESS_BED"]
    df = df.drop_duplicates(subset = keys)
    
    # manually edit those with duplicated key: ["NAME", "ADDRESS", "CITY", "STATE", "TYPE"]
    df = df.drop_duplicates(subset = ["NAME", "ADDRESS", "CITY", "STATE", "TYPE"], keep = False)
    df_edits = pd.read_csv(oj(out_dir, "hifld_nursinghomes_manualedits.csv"))
    # Note: for duplicates in MO: used https://health.mo.gov/information/boards/certificateofneed/pdf/rcfcty.pdf for validation
    # Nursing homes in other states were googled manually
    df = pd.concat([df, df_edits], axis = 0, sort = False)
    
    # rename columns
    df.columns = map(str.title, df.columns)
    df = df.rename(columns = {'Countyfips': 'countyFIPS'})
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    # write out to csv
    df.to_csv(oj(out_dir, "hifld_nursinghomes.csv"), header=True, index=False)
    
    return df


if __name__ == '__main__':
    df = clean_hifld_nursinghomes()
    print("cleaned hifld_nursinghomes successfully.")

