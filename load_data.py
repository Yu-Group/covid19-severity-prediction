import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from functions import merge_data
from os.path import join as oj
import os
from sklearn.model_selection import train_test_split
import re
from functions import preprocess
from functions import load_usafacts_data


def load_county_level(
        data_dir='data',
        cached_file='df_county_level_cached.pkl',
        cached_file_abridged='df_county_level_abridged_cached.csv',
        ahrf_data='hrsa/data_AHRF_2018-2019/processed/df_renamed.pkl',
        diabetes='diabetes/DiabetesAtlasCountyData.csv',
        voting='voting/county_voting_processed.pkl',
        icu='medicare/icu_county.csv',
        heart_disease_data="cardiovascular_disease/heart_disease_mortality_data.csv",
        stroke_data="cardiovascular_disease/stroke_mortality_data.csv",
        unacast="unacast/Unacast_Social_Distancing_Latest_Available_03_23.csv"
    ):
    '''
    Params
    ------
    data_dir 
        path to the data directory
    cached_file
        path to the cached file (within the data directory)
    '''
    df_covid = load_usafacts_data.load_daily_data(dir_mod=data_dir)
    
    cached_file = oj(data_dir, cached_file)
    cached_file_abridged = oj(data_dir, cached_file_abridged)
    ahrf_data = oj(data_dir, ahrf_data)
    diabetes = oj(data_dir, diabetes)
    voting = oj(data_dir, voting)
    icu = oj(data_dir, icu)
    heart_disease_data = oj(data_dir, heart_disease_data)
    stroke_data = oj(data_dir, stroke_data)
    unacast = oj(data_dir, unacast)

    # look for cached file in data_dir
    if os.path.exists(cached_file):
        df = pd.read_pickle(cached_file)
        return pd.merge(df, df_covid, on='countyFIPS')

    # otherwise run whole pipeline
    print('loading county level data...')
    df = merge_data.merge_data(ahrf_data=ahrf_data,
                               medicare_group="All Beneficiaries",
                               voting=voting,
                               icu=icu,
                               resp_group="Chronic respiratory diseases",
                               heart_disease_data=heart_disease_data,
                               stroke_data=stroke_data,
                               diabetes=diabetes,
                               unacast=unacast)  # also cleans usafacts data

    # basic preprocessing
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.infer_objects()

    # add features
    df = preprocess.add_features(df)

    # write cached file
    print('caching to', cached_file)
    df.to_pickle(cached_file)
    important_vars = important_keys(df)
    df[important_vars].to_csv(cached_file_abridged)

    # add covid data
    df = pd.merge(df, df_covid, on='countyFIPS')

    return df


def load_hospital_level(data_dir='data_hospital_level',
                        merged_hospital_level_info='processed/04_hospital_level_info_merged_with_website.csv',
                        fips_info='processed/02_county_FIPS.csv'):
    '''
    Params
    ------
    data_dir 
        path to the hospital data directory
    '''
    merged_hospital_level_info = oj(data_dir, merged_hospital_level_info)
    fips_info = oj(data_dir, fips_info)
    county_fips = pd.read_csv(fips_info)
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

    hospital_level['countyFIPS'] = hospital_level.apply(lambda x: map_county_to_fips(x['County Name_x'], x['State_x']),
                                                        axis=1).astype('float')
    hospital_level['IsAcademicHospital'] = (pd.isna(hospital_level['TIN'])==False).astype(int)
    hospital_level['IsUrbanHospital'] = (hospital_level['Urban or Rural Designation'] == 'Urban').astype(int)
    hospital_level['IsAcuteCareHospital'] = (hospital_level['Hospital Type'] == 'Acute Care Hospitals').astype(int)
    
    # rename keys
    remap = {
        '#ICU_beds': 'ICU Beds in County', 
        'Total Employees': 'Hospital Employees',
        'County Name_x': 'County Name',
        'Facility Name_x': 'Facility Name'
    }
    hospital_level = hospital_level.rename(columns=remap)
    
    return hospital_level


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
    comorbidity_hrsa = ['#EligibleforMedicare2018', 'MedicareEnrollment,AgedTot2017', '3-YrDiabetes2015-17']
    comorbidity_misc = ["DiabetesPercentage", "HeartDiseaseMortality", "StrokeMortality", "Smokers_Percentage", 'Respiratory Mortality']
    comorbidity = comorbidity_hrsa + comorbidity_misc

    # political leanings (ratio of democrat : republican votes in 2016 presidential election)
    political = ['dem_to_rep_ratio']
    
    social_dist = ['unacast_n_grade', 'unacast_daily_distance_diff']

    important_vars = demographics + comorbidity + hospitals + political + age_distr + mortality + social_dist
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
    print(df.shape)
    print('data including', 
          [k for k in df.keys() if '#Deaths' in k][-1],
          [k for k in df.keys() if '#Cases' in k][-1])

    
def city_to_countFIPS_dict(df):
    '''
    '''
    # city to countyFIPS dict
    r = df[['countyFIPS', 'City']]
    dr = {}
    for i in range(r.shape[0]):
        row = r.iloc[i]
        if not row['City'] in dr:
            dr[row['City']] = row['countyFIPS']
        elif row['City'] in dr and not np.isnan(row['countyFIPS']):
            dr[row['City']] = row['countyFIPS']