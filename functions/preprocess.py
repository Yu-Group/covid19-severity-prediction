import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from functions import merge_data
from functions import load_medicare_data
from functions import load_respiratory_disease_data
from functions import load_tobacco_use_data
from os.path import join as oj
import os
from sklearn.model_selection import train_test_split
import re

def add_features(df):
    df['FracMale2017'] = df['PopTotalMale2017'] / (df['PopTotalMale2017'] + df['PopTotalFemale2017'])
    df['#FTEHospitalTotal2017'] = df['#FTETotalHospitalPersonnelShortTermGeneralHospitals2017'] + df['#FTETotalHospitalPersonnelSTNon-Gen+LongTermHosps2017']
    
    # add estimated mortality
    age_distr = list([k for k in df.keys() if 'pop' in k.lower() 
                      and '2010' in k
                      and ('popmale' in k.lower() or 'popfmle' in k.lower())])
    mortality = [k for k in df.keys() if 'mort' in k.lower() 
             and '2015-17' in k.lower()]
    
    pop = [age_distr[:2], age_distr[2:6], age_distr[6:10],
       age_distr[10:14], age_distr[14:16], age_distr[16:18],
       age_distr[18:22], age_distr[22:24], age_distr[24:26],
       age_distr[26:]]
    mort = [mortality[:2], mortality[2], mortality[3],
        mortality[4], mortality[5], mortality[6],
        mortality[7], mortality[8], mortality[9],
        mortality[10]]
    
    def weighted_sum(df, keys_list1, keys_list2):
        vals = np.zeros(df.shape[0])
        for i in range(len(keys_list1)):
            vals1 = (1.0 * df[keys_list1[i]]) 
            vals2 = df[keys_list2[i]]
            if len(vals1.shape) > 1:
                vals1 = vals1.sum(axis=1)
            if len(vals2.shape) > 1:
                vals2 = vals2.sum(axis=1)
            vals1 = vals1 / df['CensusPopulation2010']
            vals += vals1.values * vals2.values
        return vals
    df['mortality2015-17Estimated'] = weighted_sum(df, pop, mort)
    
    
    return df