import pandas as pd
import numpy as np
from os.path import join as oj

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
    
    usafacts_data_cases = oj(data_dir, 'confirmed_cases.csv')
    usafacts_data_deaths = oj(data_dir, 'deaths.csv')
  
    cases = pd.read_csv(usafacts_data_cases, encoding="iso-8859-1", index_col=0).T
    deaths = pd.read_csv(usafacts_data_deaths, encoding="iso-8859-1", index_col=0).T
    if not 'countyFIPS' in deaths.keys():
        deaths = pd.read_csv(usafacts_data_deaths, encoding="utf-8", index_col=0).T
    # change to int type
    for col in cases.columns:
        if not 'county' in col.lower() and not 'state' in col.lower():
            cases[col] = cases[col].astype(float).astype(int)
            deaths[col] = deaths[col].astype(float).astype(int)
    # rename column names
    cases = cases.rename(columns={k: '#Cases_' + k for k in cases.keys()
                                  if not 'county' in k.lower()
                                  and not 'state' in k.lower()})

    deaths = deaths.rename(columns={k: '#Deaths_' + k for k in deaths.keys()
                                    if not 'county' in k.lower()
                                    and not 'state' in k.lower()})

    deaths.countyFIPS = deaths.countyFIPS.astype(int)
    cases.countyFIPS = cases.countyFIPS.astype(int)
    cases = cases[cases.countyFIPS != 0]  # ignore cases where county is unknown
    cases = cases.groupby(['countyFIPS']).sum().reset_index()  # sum over duplicate counties
    deaths = deaths[deaths.countyFIPS != 0]
    deaths = deaths.groupby(['countyFIPS']).sum().reset_index()

    df = pd.merge(cases, deaths, how='left', on='countyFIPS')
    df = df.fillna(0)
    
    # add time-series keys
    deaths_keys = [k for k in df.keys() if '#Deaths' in k and not 'Unnamed' in k]
    cases_keys = [k for k in df.keys() if '#Cases' in k and not 'Unnamed' in k]
    deaths = df[deaths_keys].values
    cases = df[cases_keys].values
    df['deaths'] = [deaths[i] for i in range(deaths.shape[0])]
    df['cases'] = [cases[i] for i in range(cases.shape[0])]
    df['tot_deaths'] = deaths[:, -1]
    df['tot_cases'] = cases[:, -1]
    
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    
    return df
