#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_ca_hospitalizations(data_dir='.'):
    ''' Load in CA Hospitalizations data
    
    Parameters
    ----------
    data_dir : str; path to the data directory to save 
               raw data
    
    Returns
    -------
    data frame
    '''
    
    raw = pd.read_csv("https://data.chhs.ca.gov/dataset/6882c390-b2d7-4b9a-aefa-2068cee63e47/resource/6cd8d424-dfaa-4bdd-9410-a3d656e1176e/download/covid19data.csv")
    
    raw.to_csv(oj(data_dir, "ca_hospitalizations.csv"), index = False)
    
    return raw

if __name__ == '__main__':
    raw = load_ca_hospitalizations()
    print('loaded ca_hospitalizations successfully.')

