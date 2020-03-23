import numpy as np
import pandas as pd
from functions import load_medicare_data
from functions import load_respiratory_disease_data
from os.path import join as oj


def merge_data(ahrf_data, usafacts_data_cases, diabetes, voting,
               medicare_group="All Beneficiaries", 
               resp_group="Chronic respiratory diseases"):
    
    # read in data
    facts = pd.read_pickle(ahrf_data)
    facts = facts.rename(columns={'Blank': 'id'})
    cases = pd.read_csv(usafacts_data_cases, encoding="iso-8859-1")
    cases = cases.rename(columns={k: '#Cases_' + k for k in cases.keys() 
                                  if not 'county' in k.lower()
                                  and not 'state' in k.lower()})
    chronic_all_orig = load_medicare_data.loadChronicSheet(medicare_group)
    diabetes = pd.read_csv(diabetes, skiprows = 2, skipfooter = 1)
    diabetes = diabetes[["CountyFIPS", "Percentage"]]
    diabetes.columns = ["countyFIPS", "Diabetes Percentage"]
    resp_disease = load_respiratory_disease_data.loadRespDiseaseSheet(resp_group)
    cases = cases[cases.countyFIPS != 0]
    voting = pd.read_pickle(voting)

    # raw.iloc[224, 0] = 13245 # fix err with Richmond, Georgia

    # sum over duplicate counties
    # cases = cases.groupby(['countyFIPS', 'County Name', 'State', 'stateFIPS']).sum().reset_index()
    
    # clean data
    cases = cases.groupby(['countyFIPS']).sum().reset_index()
    facts['countyFIPS'] = facts['Header-FIPSStandCtyCode'].astype(int)
    chronic_all_orig['countyFIPS'] = chronic_all_orig['countyFIPS'].astype(int)
    
    # merge data
    df = pd.merge(facts, cases, on='countyFIPS')
    df = pd.merge(df, chronic_all_orig, on='countyFIPS')
    df = pd.merge(df, diabetes, on='countyFIPS')
    df = pd.merge(df, resp_disease, on='countyFIPS')
    df = pd.merge(df, voting, on='countyFIPS')
    return df


    
    