#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_brfss_smoking(data_dir='.'):
    ''' Load in BRFSS Adult Smoking data (2017)
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing 
               ./state_data/brfss_smoking_STATENAME.XLSX
    
    Returns
    -------
    data frame
    '''
    
    states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
              'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 
              'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 
              'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 
              'Nebraska', 'Nevada', 'New%20Hampshire', 'New%20Jersey', 'New%20Mexico', 
              'New%20York', 'North%20Carolina', 'North%20Dakota', 'Ohio', 'Oklahoma', 'Oregon', 
              'Pennsylvania', 'Rhode%20Island', 'South%20Carolina', 'South%20Dakota', 
              'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
              'West%20Virginia', 'Wisconsin', 'Wyoming', 'District%20of%20Columbia']
    raw_ls = []
    for state in states:
        raw = pd.read_excel(oj(data_dir, 'state_data', 'brfss_smoking_' + state + '.xlsx'), 
                           sheet_name = 'Ranked Measure Data', 
                           skiprows = 1)
        id_idx = raw.columns.get_loc('FIPS')
        smoking_idx = raw.columns.get_loc('% Smokers')
        raw = raw.iloc[:, [id_idx, smoking_idx, smoking_idx + 1, smoking_idx + 2]]
        raw_ls.append(raw)
    raw = pd.concat(raw_ls)
    
    return raw

if __name__ == '__main__':
    raw = load_brfss_smoking()
    print('loaded brfss_smoking successfully.')

