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
import functions import preprocess
#from load_data import load_county_level

outcome_cases = '#Cases_3/23/2020'
outcome_deaths = '#Deaths_3/23/2020'

def load_county_level(ahrf_data = 'data/hrsa/data_AHRF_2018-2019/processed/df_renamed.pkl',
        usafacts_data_cases = 'data/usafacts/confirmed_cases.csv',
        usafacts_data_deaths = 'data/usafacts/deaths.csv',
        diabetes = 'data/diabetes/DiabetesAtlasCountyData.csv',
        voting = 'data/voting/county_voting_processed.pkl',
        icu = 'data/medicare/icu_county.csv',
        heart_disease_data = "data/cardiovascular_disease/heart_disease_mortality_data.csv",
        stroke_data = "data/cardiovascular_disease/stroke_mortality_data.csv",
        use_cached=True,
        cached_file='data/df_county_level_cached.pkl'):
    
    if use_cached and os.path.exists(cached_file):
        return pd.read_pickle(cached_file)
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
    
    # basic preprocessing
    df = df.loc[:,~df.columns.duplicated()]
    df = df.sort_values(outcome_deaths, ascending=False)
    df = df.infer_objects()
    
    # add features
    df = preprocess.add_features(df)
    
    if use_cached:
        df.to_pickle(cached_file)
    
    return df


def merge_hospital_and_county_data(hospital_info_keys, county_info_keys,
                                   merged_hospital_level_info = 'data_hospital_level/processed/hospital_level_info_merged.csv',
#                                    hospital_info = 'data/02_county_FIPS.csv'):                                   
                                   fips_info = 'data_hospital_level/processed/02_county_FIPS.csv'):
    
    county_fips = pd.read_csv(fips_info)
    #print(hospitals.keys())
    county_fips['COUNTY'] = county_fips.apply(lambda x: re.sub('[^a-zA-Z]+', '', x['COUNTY']).lower(), axis=1)
    county_to_fips = dict(zip(zip(county_fips['COUNTY'], county_fips['STATE']), county_fips['COUNTYFIPS']))
    hospital_level = pd.read_csv(merged_hospital_level_info)
    def map_county_to_fips(name, st):
        if type(name) is str:
            index = name.find(' County, ')
            name = name[:index]
            name = re.sub('[^a-zA-Z]+', '', name).lower()
            if (name, st) in county_to_fips:
                return int(county_to_fips[(name, st)])
        return np.nan
    hospital_level['countyFIPS'] = hospital_level.apply(lambda x: map_county_to_fips(x['County Name_x'], x['State_x']), axis=1).astype('float')
    county_level = load_county_level()
    if county_info_keys != 'all':
        county_level = county_level[county_info_keys]
    if hospital_info_keys != 'all':
        hospital_level = hospital_level[hospital_info_keys]
    hospital_county_merged = hospital_level.merge(county_level, how='left', on='countyFIPS')
    return hospital_county_merged

def important_keys(df):
    demographics = ['PopulationEstimate2018', 'Population(Persons)2017',  
                    'PopTotalMale2017', 'PopTotalFemale2017', 'FracMale2017',
                    'PopulationEstimate65+2017',
                    'PopulationDensityperSqMile2010',
                    'CensusPopulation2010',
                    'MedianAge2010', 'MedianAge,Male2010', 'MedianAge,Female2010']

    # hospital vars
    hospitals_hrsa = ['#FTEHospitalTotal2017', "TotalM.D.'s,TotNon-FedandFed2017", '#HospParticipatinginNetwork2017']
    hospitals_misc = ["#Hospitals", "#ICU_beds"]
    hospitals = hospitals_hrsa + hospitals_misc

    age_distr = list([k for k in df.keys() if 'pop' in k.lower() 
                      and '2010' in k
                      and ('popmale' in k.lower() or 'popfmle' in k.lower())])
    mortality = [k for k in df.keys() if 'mort' in k.lower() 
                 and '2015-17' in k.lower()]

    # comorbidity (simultaneous presence of multiple conditions) vars
    comorbidity_hrsa = [ '#EligibleforMedicare2018',  'MedicareEnrollment,AgedTot2017', '3-YrDiabetes2015-17']
    comorbidity_misc = ["DiabetesPercentage", "HeartDiseaseMortality", "StrokeMortality", "Smokers_Percentage"]
    comorbidity = comorbidity_hrsa + comorbidity_misc

    # political leanings (ratio of democrat : republican votes in 2016 presidential election)
    political = ['dem_to_rep_ratio']

    important_vars = demographics + comorbidity + hospitals + political + age_distr + mortality
    return important_vars

def split_data_by_county(df):
    np.random.seed(42)
    countyFIPS = df.countyFIPS.values
    fips_train, fips_test = train_test_split(countyFIPS, test_size=0.25, random_state=42)
    df_train = df[df.countyFIPS.isin(fips_train)]
    df_test = df[df.countyFIPS.isin(fips_test)]
    return df_train, df_test

if __name__ == '__main__':
    df = load_county_level()
    print('loaded succesfully')