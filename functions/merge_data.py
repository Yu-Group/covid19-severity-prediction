import numpy as np
import pandas as pd
from functions import load_medicare_data
from functions import load_respiratory_disease_data
from functions import load_tobacco_use_data
from functions import load_mortality_data
from os.path import join as oj


def merge_data(ahrf_data, 
               diabetes, 
               voting,
               icu,
               heart_disease_data,
               stroke_data,
               unacast,
               medicare_group="All Beneficiaries", 
               resp_group="Chronic respiratory diseases"):
    
    # read in data
    facts = pd.read_pickle(ahrf_data)
    facts = facts.rename(columns={'Blank': 'id'})
    
    ## Medicare data risk factors
    chronic_all_orig = load_medicare_data.loadChronicSheet(medicare_group)
    
    ## risk factors data (not from Medicare)
    tobacco = load_tobacco_use_data.loadTobaccoData()
    
    diabetes = pd.read_csv(diabetes, skiprows = 2, skipfooter = 1)
    diabetes = diabetes[["CountyFIPS", "Percentage"]]
    diabetes.columns = ["countyFIPS", "DiabetesPercentage"]
    
    heart_disease = pd.read_csv(heart_disease_data, na_values = [-1, ""])
    heart_disease = heart_disease[["cnty_fips", "Value"]]
    heart_disease.columns = ["countyFIPS", "HeartDiseaseMortality"]
    
    stroke = pd.read_csv(stroke_data, na_values = [-1, ""])
    stroke = stroke[["cnty_fips", "Value"]]
    stroke.columns = ["countyFIPS", "StrokeMortality"]
    
    resp_disease = load_respiratory_disease_data.loadRespDiseaseSheet(resp_group)
    print('ks', resp_disease.keys())
    ## end of risk factors data (not from Medicare)
    
    ## unacast social distancing data
    unacast = pd.read_csv(unacast)
    unacast = unacast[["FIPS", "grade", "n_grade", 
                       "daily_distance_diff", "county_population", "Shape__Area"]]
    unacast = unacast.rename(columns={'FIPS': 'countyFIPS', 
                                      'grade': 'unacast_grade', 
                                      'n_grade': 'unacast_n_grade', 
                                      'daily_distance_diff': 'unacast_daily_distance_diff', 
                                      'county_population': 'unacast_county_pop', 
                                      'Shape__Area': 'unacast_county_area'})
    
    ## load mortality data
    mortality = load_mortality_data.loadMortalityData()
    
    ## load icu data
    icu = pd.read_csv(icu)
    icu = icu[["cnty_fips", "hospitals", "icu_beds"]]
    icu.columns = ["countyFIPS", "#Hospitals", "#ICU_beds"]
    
    ## load voting data
    voting = pd.read_pickle(voting)

    # raw.iloc[224, 0] = 13245 # fix err with Richmond, Georgia

    # clean data
    facts['countyFIPS'] = facts['Header-FIPSStandCtyCode'].astype(int)
    chronic_all_orig['countyFIPS'] = chronic_all_orig['countyFIPS'].astype(int)
    
    # merge data
    df = facts
    df = df.fillna(0)
    df = pd.merge(df, chronic_all_orig, on='countyFIPS')
    df = pd.merge(df, diabetes, on='countyFIPS')
    df = pd.merge(df, resp_disease, on='countyFIPS')
    df = pd.merge(df, voting, on='countyFIPS')
    df = pd.merge(df, icu, on='countyFIPS')
    df = pd.merge(df, heart_disease, on='countyFIPS')
    df = pd.merge(df, stroke, on='countyFIPS')
    df = pd.merge(df, tobacco, on='countyFIPS')
    df = pd.merge(df, unacast, on='countyFIPS')
    df = pd.merge(df, mortality, on='countyFIPS')
    return df


def merge_county_and_hosp(df_county, df_hospital):
    outcomes = ['tot_cases', 'tot_deaths']
    df = df_hospital.merge(df_county, how='left', on='countyFIPS')
    df[outcomes] = df[outcomes].fillna(0)

    # aggregate employees by county
    total_emp_county = df.groupby('countyFIPS').agg({'Hospital Employees': 'sum'})
    total_emp_county = total_emp_county.rename(columns={'Hospital Employees': 'Hospital Employees in County'})
    df_county = pd.merge(df_county, total_emp_county, how='left', on='countyFIPS')
    df = pd.merge(df, total_emp_county, how='left', on='countyFIPS')

    # filter hospitals
    df = df[~df['countyFIPS'].isna()] # & df['IsAcademicHospital'] & df['Hospital Employees'] > 0]
    df = df.sort_values(by=['tot_deaths', 'Hospital Employees'], ascending=False)


    # fraction of employees out of all county hospitals
    df['Frac Hospital Employees of County'] = df['Hospital Employees'] / df['Hospital Employees in County']
    return df