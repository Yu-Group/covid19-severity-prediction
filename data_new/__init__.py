#!/usr/bin/python3

import numpy as np
import pandas as pd
import os
from os.path import join as oj
import sys

from .county_level.raw.usafacts_infections.load import load_usafacts_infections
from .county_level.processed.ahrf_health.clean import clean_ahrf_health
from .county_level.processed.cdc_svi.clean import clean_cdc_svi
from .county_level.processed.chrr_smoking.clean import clean_chrr_smoking
from .county_level.processed.dhdsp_heart.clean import clean_dhdsp_heart
from .county_level.processed.dhdsp_stroke.clean import clean_dhdsp_stroke
from .county_level.processed.hpsa_shortage.clean import clean_hpsa_shortage
from .county_level.processed.ihme_respiratory.clean import clean_ihme_respiratory
from .county_level.processed.khn_icu.clean import clean_khn_icu
from .county_level.processed.medicare_chronic.clean import clean_medicare_chronic
from .county_level.processed.mit_voting.clean import clean_mit_voting
from .county_level.processed.nchs_mortality.clean import clean_nchs_mortality
from .county_level.processed.unacast_mobility.clean import clean_unacast_mobility
from .county_level.processed.usdss_diabetes.clean import clean_usdss_diabetes
from .county_level.processed.jhu_interventions.clean import clean_jhu_interventions


def load_county(data_dir=".", cached_file="county_data.csv", 
                cached_abridged_file="county_data_abridged.csv",
                cached=True, abridged=True, infections_data="usafacts", rm_na=True):
    '''  Load in merged county data set
    
    Parameters
    ----------
    data_dir : string; path to the data directory
    
    cached_file : string; name of cached county-level data
    
    cached_abridged_file : string; name of cached abridged county-level data
    
    cached : logical; whether or not to load in cached data (if possible)
    
    abridged : logical; whether or not to load in abridged data
    
    infections_data : string; source for daily cases/deaths counts from
                      COVID-19 infections; must be either 'usafacts' or 'nytimes'
    
    rm_na : logical; whether or not to remove counties with NA cases or deaths
    
    Returns
    -------
    data frame with abridged or full county-level data set
    '''
    
    # error checking
    if infections_data not in ['usafacts', 'nytimes']:
        raise ValueError("infections_data must be either 'usafacts' or 'nytimes'")
    
    # data directories
    orig_dir = os.getcwd()
    data_dir_raw = oj(data_dir, "county_level", "raw")
    data_dir_clean = oj(data_dir, "county_level", "processed")
    
    if cached == True:  
        # read in cached data
        if abridged == True:
            if os.path.exists(oj(data_dir, cached_abridged_file)):
                cnty = pd.read_csv(oj(data_dir, cached_abridged_file))
            else:
                raise ValueError("Cached abridged file cannot be found. " +
                                 "Please set cached = False.")
        else:
            if os.path.exists(oj(data_dir, cached_file)):
                cnty = pd.read_csv(oj(data_dir, cached_file))
            else:
                raise ValueError("Cached file cannot be found. " + 
                                 "Please set cached = False")
        
    else: 
        # generate county data
        datasets = ["ahrf_health", "cdc_svi", "chrr_smoking", "dhdsp_heart",
                    "dhdsp_stroke", "hpsa_shortage", "ihme_respiratory", "khn_icu",
                    "medicare_chronic", "mit_voting", "nchs_mortality", 
                    "unacast_mobility", "usdss_diabetes", "jhu_interventions"]
        df_ls = []
        for dataset in datasets:
            # check if raw data files exist locally
            if dataset == "chrr_smoking":
                if len(os.listdir(oj(data_dir_raw, dataset, "state_data"))) != 51:
                    # download raw data
                    os.chdir(oj(data_dir_raw, dataset))
                    os.system("python3 download.py")
                    print("downloaded " + dataset + " successfully")
                    os.chdir(orig_dir)
            elif dataset == "unacast_mobility":  # private data
                if not "unacast_mobility.csv" in os.listdir(oj(data_dir_raw, dataset)):
                    continue
            elif dataset != "jhu_interventions":
                if not any(fname.startswith(dataset) \
                           for fname in os.listdir(oj(data_dir_raw, dataset))):
                    # download raw data
                    os.chdir(oj(data_dir_raw, dataset))
                    os.system("python3 download.py")
                    print("downloaded " + dataset + " successfully")
                    os.chdir(orig_dir)
                
            # clean data
            os.chdir(oj(data_dir_clean, dataset))
            df_ls.append(eval("clean_" + dataset + "()"))
            print("loaded and cleaned " + dataset + " successfully")
            os.chdir(orig_dir)
            
        # merge county data
        cnty_fips = pd.read_csv(oj(data_dir_raw, "county_ids", "county_fips.csv"))
        cnty_fips["countyFIPS"] = cnty_fips["countyFIPS"].str.zfill(5)
        cnty_latlong = pd.read_csv(oj(data_dir_raw, "county_ids", "county_latlong.csv"))
        cnty_latlong = cnty_latlong[["countyFIPS", "lat", "lon"]]
        cnty_latlong["countyFIPS"] = cnty_latlong["countyFIPS"].astype(str).str.zfill(5)
        cnty = pd.merge(cnty_fips, cnty_latlong, on="countyFIPS", how="left")
        for i in range(0, len(df_ls)):
            df_ls[i] = clean_id(df_ls[i])  # remove potentially duplicate ID columns
            cnty = pd.merge(cnty, df_ls[i], on='countyFIPS', how="left")  # merge data
            
        # basic preprocessing
        cnty = cnty.loc[:, ~cnty.columns.duplicated()]
        cnty = cnty.infer_objects()
        
        # add new features
        cnty = add_features(cnty)
        
        if abridged == True:
            # get shortlist of important variables for abridged data set
            id_vars = ["countyFIPS", 'CountyName', 'StateName', 'lat', 'lon']
            important_vars = id_vars + important_keys(cnty)
            cnty = cnty[important_vars]
            cnty.to_csv(oj(data_dir, "county_data_abridged.csv"), header=True, index=False)
            print("saved county_data_abridged.csv successfully")
        else:
            # write full county data to file
            cnty.to_csv(oj(data_dir, "county_data.csv"), header=True, index=False)
            print("saved county_data.csv successfully")
        
    # get covid-19 infections data
    if infections_data == 'usafacts':
        covid = load_usafacts_infections(oj(data_dir_raw, "usafacts_infections"))
    elif infections_data == 'nytimes':
        raise ValueError('infections_data = "nytimes" not yet implemented')
        
    # merge county data with covid data
    df = pd.merge(cnty, covid, on='countyFIPS', how='left')
    df = df.sort_values('tot_deaths', ascending=False)
    
    # remove NA cases or deaths for prediction models
    if rm_na == True:
        df = df.dropna(subset = ['cases', 'deaths'])

    return df


def clean_id(df):
    '''  Remove potentially duplicate ID columns (e.g., "State", "State Name", "County",
    "County Name", "Location")
    
    Parameters
    ----------
    df : data frame
    
    Returns
    -------
    data frame without columns named "State", "State Name", "County", "County Name",
    "Location"
    '''
    
    drop_keys = ["State", "State Name", "County", "County Name", "Location"]
    for key in drop_keys:
        if key in df.columns:
            df = df.drop(columns = key)
            
    return df


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


def important_keys(df):
    # demographic variables
    demographics = ['PopulationEstimate2018',
                    'PopTotalMale2017', 'PopTotalFemale2017', 'FracMale2017',
                    'PopulationEstimate65+2017',
                    'PopulationDensityperSqMile2010',
                    'CensusPopulation2010',
                    'MedianAge2010',
                    #'MedianAge,Male2010', 'MedianAge,Female2010',
                   ]

    # hospital variables
    hospitals_hrsa = ['#FTEHospitalTotal2017', "TotalM.D.'s,TotNon-FedandFed2017", '#HospParticipatinginNetwork2017']
    hospitals_misc = ["#Hospitals", "#ICU_beds"]
    hospitals = hospitals_hrsa + hospitals_misc

    # age distribution
    age_distr = list([k for k in df.keys() if 'pop' in k.lower()
                      and '2010' in k
                      and ('popmale' in k.lower() or 'popfmle' in k.lower())])
    
    # mortality rates
    mortality = [k for k in df.keys() if 'mort' in k.lower()
                 and '2015-17' in k.lower()]

    # comorbidity (simultaneous presence of multiple conditions) vars
    comorbidity_hrsa = ['#EligibleforMedicare2018', 'MedicareEnrollment,AgedTot2017',
                        '3-YrDiabetes2015-17']
    comorbidity_misc = ["DiabetesPercentage", "HeartDiseaseMortality", "StrokeMortality", 
                        "Smokers_Percentage", 'RespMortalityRate2014']
    comorbidity = comorbidity_hrsa + comorbidity_misc

    # political leanings (ratio of democrat : republican votes in 2016 presidential election)
    political = ['dem_to_rep_ratio']
    
    # social mobility data
    social_dist = ['unacast_n_grade', 'unacast_daily_distance_diff']
    social_dist_daily = [var for var in list(df.columns) if "daily_distance_diff" in var]
    interventions = ['stay at home', '>50 gatherings', '>500 gatherings', 'public schools', 'restaurant dine-in', 'entertainment/gym', 'federal guidelines', 'foreign travel ban']
    social =  social_dist + social_dist_daily + interventions
    
    # resource shortages/social vulnerability
    vulnerability = ['SVIPercentile', 'HPSAShortage', 'HPSAServedPop', 'HPSAUnderservedPop']

    # get list of important variables
    important_vars = demographics + comorbidity + hospitals + political + age_distr + mortality + social
    
    # keep variables that are in df
    important_vars = [var for var in important_vars if var in list(df.columns)]

    return important_vars