#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os
from datetime import datetime

from ...raw.streetlight_vmt.load import load_streetlight_vmt

def clean_streetlight_vmt(data_dir='../../../../../covid-19-private-data',
                          out_dir='.'):
    ''' Clean Streetlight Vehicle Miles Traveled Data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # load in data
    df = load_streetlight_vmt(data_dir = data_dir)
    
    # get population data
    pop = pd.read_csv(oj(out_dir, "../../raw/county_ids/county_popcenters.csv"))
    
    # create countyFIPS field
    df["countyFIPS"] = df["statefp10"].astype(str).str.zfill(2) +\
        df["countyfp10"].astype(str).str.zfill(3)
    pop["countyFIPS"] = pop["STATEFP"].astype(str).str.zfill(2) +\
        pop["COUNTYFP"].astype(str).str.zfill(3)
    
    # merge population and vmt data
    df = pd.merge(df, pop[["countyFIPS", "POPULATION"]], on="countyFIPS", how="left")
    
    # drop features
    drop_keys = ['statefp10', 'countyfp10']
    df = df.drop(columns = drop_keys)
    
    # rename features
    remap = {
        'ref_dt': 'Date',
        'county_vmt': 'VMT',
        'jan_avg_vmt': 'Jan_VMT',
        'POPULATION': 'Pop'
    }
    df = df.rename(columns = remap)
    
    # feature engineering
    df["VMT_percent_change"] = (df["VMT"] - df["Jan_VMT"]) / df["Jan_VMT"] * 100
    df["VMT_per_capita"] = df["VMT"] / df["Pop"]
    df = df.drop(columns = ["Pop", "Jan_VMT", "VMT"])
    
    # format dates
    df["Date"] = pd.to_datetime(df["Date"]).astype(str)
    
    # convert to wide format
    df = df.pivot(index = 'countyFIPS', columns = 'Date', 
                  values = ['VMT_percent_change', 'VMT_per_capita'])
    df = pd.DataFrame(df.to_records())
    df.columns = [col.replace("('", "").replace("', '", "").replace("')", "") \
                  for col in df.columns]
    
    # write out to csv
    df.to_csv(oj(out_dir, "streetlight_vmt.csv"), header=True, index=False)
    
    return df

if __name__ == '__main__':
    df = clean_streetlight_vmt()
    print("cleaned streetlight_vmt successfully.")
