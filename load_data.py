import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from os.path import join as oj
import os
from sklearn.model_selection import train_test_split
import re
import data

def load_county_level(data_dir='data'):
    '''
    Params
    ------
    data_dir 
        path to the data directory
    Saves 'county_data_abridged.csv' to data file
    '''

    if not "county_data_abridged.csv" in os.listdir(data_dir):
        df = data.load_county_data(data_dir=data_dir, cached=False)
    else:
        df = data.load_county_data(data_dir=data_dir, cached=True)
    return df.sort_values("tot_deaths", ascending=False)
    


def load_hospital_level(data_dir='data_hospital_level',
                        merged_hospital_level_info='hospital_info_private.csv',
                        fips_info='county_FIPS.csv'):
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
    demographics = ['PopulationEstimate2018',
                    'PopTotalMale2017', 'PopTotalFemale2017', 'FracMale2017',
                    'PopulationEstimate65+2017',
                    'PopulationDensityperSqMile2010',
                    'CensusPopulation2010',
                    'MedianAge2010',
#                     'MedianAge,Male2010', 'MedianAge,Female2010',
                   ]

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
    
    # keep variables that are in df
    important_vars = [var for var in important_vars if var in list(df.columns)]
    
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
