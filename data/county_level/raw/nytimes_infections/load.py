#! /home/ubuntu/anaconda3/bin/python3

import pandas as pd
import numpy as np
from os.path import join as oj

def load_nytimes_infections(data_dir="."):
    raw = pd.read_csv(oj(data_dir, 'nytimes_infections.csv') , dtype={"fips":str})
    raw['date'] = pd.to_datetime(raw['date']).apply(lambda x: x.strftime("%m-%d-%Y"))
    raw['countyFIPS'] = raw['fips']
    raw = raw.reindex(sorted(raw.columns), axis=1)

    # add NYC and Kansas
    raw.loc[raw['county'] == 'New York City', 'countyFIPS'] = 'City1'
    raw.loc[raw['county'] == 'Kansas City', 'countyFIPS'] = 'City2'

    # deal with confirmed
    confirmed = raw.dropna(subset=["countyFIPS"]).pivot("countyFIPS", "date", "cases")
    confirmed = confirmed.fillna(0)
    confirmed.columns = ["#Cases_" + x for x in confirmed.columns]
    # enforce monotonicity
    for col_ind in reversed(range(0,confirmed.shape[1]-1)):
        confirmed.iloc[:,col_ind] = np.minimum(
            confirmed.iloc[:,col_ind],
            confirmed.iloc[:,col_ind+1])

    # deal with deaths
    deaths = raw.dropna(subset=["countyFIPS"]).pivot("countyFIPS", "date", "deaths")
    deaths = deaths.fillna(0)
    deaths.columns = ["#Deaths_" + x for x in deaths.columns]
    # enforce monotonicity
    for col_ind in reversed(range(0,deaths.shape[1]-1)):
        deaths.iloc[:,col_ind] = np.minimum(
            deaths.iloc[:,col_ind],
            deaths.iloc[:,col_ind+1])
    return confirmed.merge(deaths, left_index=True, right_index=True).astype(int).reset_index()
    
if __name__ == "__main__":
    nytimes_infections = load_nytimes_infections()
