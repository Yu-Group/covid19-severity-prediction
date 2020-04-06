#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_jhu_interventions(data_dir='.'):
    ''' Load in JHU Interventions (county-level) data set (pulled directly from GitHub source)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to write raw jhu_interventions.csv
    
    Returns
    -------
    data frame
    '''
    
    raw = pd.read_csv("https://raw.githubusercontent.com/JieYingWu/COVID-19_US_County-level_Summaries/master/data/interventions.csv")
    raw.to_csv(oj(data_dir, "jhu_interventions.csv"), header=True, index=False)

    return raw

if __name__ == '__main__':
    raw = load_jhu_interventions()
    print('loaded jhu_interventions successfully.')



