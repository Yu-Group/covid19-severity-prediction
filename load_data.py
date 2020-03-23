import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from functions import merge_data
from functions import load_medicare_data
from functions import load_respiratory_disease_data
from os.path import join as oj

outcome_cases = '#Cases_3/22/2020'
outcome_deaths = '#Deaths_3/22/2020'

def load_county_level(ahrf_data = 'data/hrsa/data_AHRF_2018-2019/processed/df_renamed.pkl',
        usafacts_data_cases = 'data/usafacts/confirmed_cases_mar23.csv',
        usafacts_data_deaths = 'data/usafacts/deaths_mar23.csv',
        diabetes = 'data/diabetes/DiabetesAtlasCountyData.csv',
        voting = 'data/voting/county_voting_processed.pkl',
        icu = 'data/medicare/icu_county.csv',
        heart_disease_data = "data/cardiovascular_disease/heart_disease_mortality_data.csv",
        stroke_data = "data/cardiovascular_disease/stroke_mortality_data.csv"):
    print('loading county level data...')
    df = merge_data.merge_data(ahrf_data=ahrf_data, 
                               usafacts_data_cases=usafacts_data_cases,
                               usafacts_data_deaths=usafacts_data_deaths,
                               medicare_group="All Beneficiaries",
                               voting=voting,
                               icu=icu,
                               resp_group="Chronic respiratory diseases",
                               heart_disease_data=heart_disease_data,
                               stroke_data=stroke_data,
                               diabetes=diabetes) # also cleans usafacts data
    return df