import numpy as np
import pandas as pd
from functions import load_medicare_data
from functions import load_respiratory_disease_data
from functions import load_tobacco_use_data
from os.path import join as oj


def merge_data(ahrf_data, 
               usafacts_data_cases, 
               usafacts_data_deaths,
               diabetes, 
               voting,
               icu,
               heart_disease_data,
               stroke_data,
               medicare_group="All Beneficiaries", 
               resp_group="Chronic respiratory diseases"):
    
    # read in data
    facts = pd.read_pickle(ahrf_data)
    facts = facts.rename(columns={'Blank': 'id'})
    
    cases = pd.read_csv(usafacts_data_cases, encoding="iso-8859-1")
    cases = cases.rename(columns={k: '#Cases_' + k for k in cases.keys() 
                                  if not 'county' in k.lower()
                                  and not 'state' in k.lower()})
    
    deaths = pd.read_csv(usafacts_data_deaths, encoding="iso-8859-1")
    deaths = deaths.rename(columns={k: '#Deaths_' + k for k in deaths.keys() 
                              if not 'county' in k.lower()
                              and not 'state' in k.lower()})
    
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
    
    icu = pd.read_csv(icu)
    icu = icu[["cnty_fips", "hospitals", "icu_beds"]]
    icu.columns = ["countyFIPS", "#Hospitals", "#ICU_beds"]
    
    voting = pd.read_pickle(voting)

    # raw.iloc[224, 0] = 13245 # fix err with Richmond, Georgia

    
    # clean data
    cases = cases[cases.countyFIPS != 0] # ignore cases where county is unknown
    cases = cases.groupby(['countyFIPS']).sum().reset_index() # sum over duplicate counties
    deaths = deaths[deaths.countyFIPS != 0]
    deaths = deaths.groupby(['countyFIPS']).sum().reset_index()
    facts['countyFIPS'] = facts['Header-FIPSStandCtyCode'].astype(int)
    chronic_all_orig['countyFIPS'] = chronic_all_orig['countyFIPS'].astype(int)
    
    # merge data
    df = pd.merge(facts, cases, on='countyFIPS')
    df = pd.merge(df, deaths, on='countyFIPS')
    df = pd.merge(df, chronic_all_orig, on='countyFIPS')
    df = pd.merge(df, diabetes, on='countyFIPS')
    df = pd.merge(df, resp_disease, on='countyFIPS')
    df = pd.merge(df, voting, on='countyFIPS')
    df = pd.merge(df, icu, on='countyFIPS')
    df = pd.merge(df, heart_disease, on='countyFIPS')
    df = pd.merge(df, stroke, on='countyFIPS')
    df = pd.merge(df, tobacco, on='countyFIPS')
    return df


    
    