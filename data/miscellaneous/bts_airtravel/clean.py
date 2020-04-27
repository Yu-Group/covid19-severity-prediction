#! /usr/bin/python3

import pandas as pd
from os.path import join as oj
import os
import numpy as np
import requests
import urllib

from load import load_bts_airtravel

def clean_bts_airtravel(data_dir='.'):
    ''' Clean Airline Origin and Destination Survey (DB1B) (2019)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
    
    # read in saved file if available
    orig_dir = os.getcwd()
    os.chdir(data_dir)
    if os.path.exists("bts_airtravel.csv"):
        df = pd.read_csv("bts_airtravel.csv",
                         index_col = "DEST_countyFIPS")
        df.index = df.index.astype(str).str.zfill(5)
        return df
    
    # load in data
    df = load_bts_airtravel()
    
    # keep features
    keep_keys = ['ORIGIN', 'DEST', 'PASSENGERS']
    df = df[keep_keys]
    
    # clean airport codes
    df = df.replace(to_replace = ["SCE", "FCA", "MQT", "HHH", "YUM", "SPN", "AZA", "CYF", "BKG", "AIN"], 
                    value = ["UNV", "GPI", "SAW", "HXD", "NYL", "GSN", "IWA", "CFK", "BBG", "AWI"])
    
    # airport location data
    apt_df = pd.read_csv("https://opendata.arcgis.com/datasets/831853ab8b714a81b6a3e21d0b164a4e_0.csv", 
                         usecols = ["X", "Y", "Loc_Id"])
    airports = set(list(df.ORIGIN.unique()) + list(df.DEST.unique()))
    apt_df = apt_df[apt_df.Loc_Id.isin(list(airports))]
    
    # get county FIPS from lat/long
    fips = []
    for index, row in apt_df.iterrows():
        lon, lat = row[["X", "Y"]]
        params = urllib.parse.urlencode({'latitude': lat, 'longitude': lon, 'format':'json'})
        response = requests.get('https://geo.fcc.gov/api/census/block/find?' + params)
        fips.append(response.json()['County']['FIPS'])
    apt_df['countyFIPS'] = fips
    
    # merge data
    df = pd.merge(df, apt_df[["Loc_Id", "countyFIPS"]], 
                  left_on="ORIGIN", right_on="Loc_Id", how="left")
    df = df.drop(columns = "Loc_Id")
    df = df.rename(columns = {"countyFIPS": "ORIGIN_countyFIPS"})
    df = pd.merge(df, apt_df[["Loc_Id", "countyFIPS"]], 
                  left_on="DEST", right_on="Loc_Id", how="left")
    df = df.drop(columns = "Loc_Id")
    df = df.rename(columns = {"countyFIPS": "DEST_countyFIPS"})
    
    # drop unknown airports (i.e., USA)
    df = df.dropna(subset = ["ORIGIN_countyFIPS", "DEST_countyFIPS"])
    
    # compute sum of passengers between two airports
    df = df.drop(columns = ["ORIGIN", "DEST"])
    df = df.groupby(["ORIGIN_countyFIPS", "DEST_countyFIPS"]).sum().reset_index()
    
    # transform to wide "adjacency" matrix
    df = df.pivot(index = 'DEST_countyFIPS', columns = 'ORIGIN_countyFIPS', 
                  values = ['PASSENGERS'])
    df = pd.DataFrame(df.to_records())
    df.columns = [col.replace("('PASSENGERS', '", "").replace("')", "") \
                  for col in df.columns]
    df = df.fillna(0)
    
    # add in all counties with/without airports
    cnty_df = pd.read_csv("../../county_level/raw/county_ids/county_fips.csv")
    cnty_df = cnty_df[~cnty_df.countyFIPS.isin(["City1", "City2"])]
    cnty_df.countyFIPS = cnty_df.countyFIPS.str.zfill(5)
    os.chdir(orig_dir)
    
    add_cnty_dest = list(set(cnty_df.countyFIPS).difference(set(df.DEST_countyFIPS)))
    add_cnty_orig = list(set(cnty_df.countyFIPS).difference(set(df.columns[1:])))
    
    zero_df = pd.DataFrame(0, index=np.arange(len(add_cnty_dest)), columns=df.columns)
    zero_df.DEST_countyFIPS = add_cnty_dest
    df = pd.concat([df, zero_df], axis=0)
    for cnty in add_cnty_orig:
        df[cnty] = 0
    
    # reorder adjacency matrix for symmetry
    df = df.set_index("DEST_countyFIPS")
    df = df.sort_index()
    df = df[sorted(df.columns.to_list())]
    
    # write out to csv
    df.to_csv(oj(data_dir, "bts_airtravel.csv"), header=True, index=True)
    
    os.system("rm -r " + oj(data_dir, 'quarter_data'))
    
    return df

if __name__ == '__main__':
    df = clean_bts_airtravel()
    print("cleaned bts_airtravel successfully.")

