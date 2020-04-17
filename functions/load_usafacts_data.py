import pandas as pd
import numpy as np
from os.path import join as oj

def load_daily_data(data_dir = "."):
    usafacts_path = oj(data_dir, "county_level/processed/usafacts_infections/usafacts_infections.csv")
    data = pd.read_csv(usafacts_path)
    data.countyFIPS = data.countyFIPS.astype(int)
    data = data[data.countyFIPS != 0]  # ignore cases where county is unknown
    
    # add time-series keys
    deaths_keys = [k for k in data.keys() if '#Deaths' in k]
    cases_keys = [k for k in data.keys() if '#Cases' in k]
    deaths = data[deaths_keys].values
    cases = data[cases_keys].values
    data['deaths'] = [deaths[i] for i in range(deaths.shape[0])]
    data['cases'] = [cases[i] for i in range(cases.shape[0])]
    data['tot_deaths'] = deaths[:, -1]
    data['tot_cases'] = cases[:, -1]
    return data
