#!/usr/bin/python3

import numpy as np
import pandas as pd
import os
from os.path import join as oj
import re
import sys

def load_nyt_nursinghomes(data_dir = '.'):
    ''' Load in NYT Nursing Home COVID-19 data
    
    Parameters
    ----------
    data_dir : str; path to the daily_data folder with raw daily files
    
    Returns
    -------
    data frame
    '''

    data = []
    for filename in os.listdir(oj(data_dir, "daily_data")):
        if not filename.endswith('.csv'):
            continue
        raw = pd.read_csv(oj(data_dir, "daily_data", filename))
        raw = raw.rename(columns = {"Cases": "Cases_" + filename[-14:-4], 
                                    "Deaths": "Deaths_" + filename[-14:-4]})
        raw["Name"] = raw["Name"].str.upper().str.strip().apply(lambda x: re.sub(' +', ' ', x))
        raw["City"] = raw["City"].str.upper().str.strip().apply(lambda x: re.sub(' +', ' ', x))
        if len(data) == 0:
            data = raw
        else:
            data = pd.merge(data, raw, on = ["Name", "City", "State"], how="outer")
    
    data.to_csv(oj(data_dir, 'nyt_nursinghomes.csv'), index=False)
    return data


if __name__ == '__main__':
    raw = load_nyt_nursinghomes()
    print('loaded nyt_nursinghomes successfully.')
