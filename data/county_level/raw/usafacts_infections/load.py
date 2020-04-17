#!/usr/bin/python3

import pandas as pd
import numpy as np
from os.path import join as oj
from datetime import datetime

def load_usafacts_infections(data_dir = "./"):
    ''' Load in USA Facts daily COVID-19 cases and deaths data
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing confirmed_cases.csv
               and deaths.csv
    
    Returns
    -------
    data frame
    '''
    pretty_date = lambda x: datetime.strftime(datetime.strptime(x, '%m/%d/%y'), '%m-%d-%Y')
    usafacts_data_cases = oj(data_dir, 'confirmed_cases.csv')
    usafacts_data_deaths = oj(data_dir, 'deaths.csv')
  
    cases = pd.read_csv(usafacts_data_cases, encoding="utf-8", index_col=0, dtype=str).T
    deaths = pd.read_csv(usafacts_data_deaths, encoding="utf-8", index_col=0, dtype=str).T
    cases.countyFIPS = cases.countyFIPS.str.zfill(5)

    deaths.countyFIPS = deaths.countyFIPS.str.zfill(5)
    # change to int type
    for col in cases.columns:
        if not 'county' in col.lower() and not 'state' in col.lower():
            cases[col] = cases[col].astype(float).astype(int)
    for col in deaths.columns:
        if not 'county' in col.lower() and not 'state' in col.lower():
            deaths[col] = deaths[col].astype(float).astype(int)
    # rename column names
    cases = cases.rename(columns={k: '#Cases_' + pretty_date(k) for k in cases.keys()
                                  if not 'county' in k.lower()
                                  and not 'state' in k.lower()})

    deaths = deaths.rename(columns={k: '#Deaths_' + pretty_date(k) for k in deaths.keys()
                                    if not 'county' in k.lower()
                                    and not 'state' in k.lower()})

    cases = cases[cases.countyFIPS != '00000']  # ignore cases where county is unknown
    cases = cases.groupby(['countyFIPS']).sum().reset_index()  # sum over duplicate counties
    deaths = deaths[deaths.countyFIPS != '00000']
    deaths = deaths.groupby(['countyFIPS']).sum().reset_index()

    df = pd.merge(cases, deaths, how='left', on='countyFIPS')
    df = df.fillna(0)

    return df

if __name__ == '__main__':
    load_usafacts_infections()
    print("load usafacts infections successfully.")
