#!/usr/bin/python3

import numpy as np
import pandas as pd
import os
from os.path import join as oj
import sys
from math import radians, sin, cos, sqrt, asin
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm
import re
import copy
#from hospital_level.processed.cms_cmi.clean import clean_cms_cmi
#from hospital_level.processed.cms_hospitalpayment.clean import clean_cms_hospitalpayment
from .county_level.processed.ahrf_health.clean import clean_ahrf_health
from .county_level.processed.cdc_svi.clean import clean_cdc_svi
from .county_level.processed.chrr_health.clean import clean_chrr_health
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
from .county_level.processed.kinsa_ili.clean import clean_kinsa_ili
from .county_level.processed.streetlight_vmt.clean import clean_streetlight_vmt
from .county_level.processed.usda_poverty.clean import clean_usda_poverty
from .county_level.processed.safegraph_socialdistancing.clean import clean_safegraph_socialdistancing
from .county_level.processed.safegraph_weeklypatterns.clean import clean_safegraph_weeklypatterns
from .county_level.processed.apple_mobility.clean import clean_apple_mobility
from .county_level.processed.google_mobility.clean import clean_google_mobility
from .nursinghome_level.processed.nyt_nursinghomes.clean import clean_nyt_nursinghomes
from .nursinghome_level.processed.hifld_nursinghomes.clean import clean_hifld_nursinghomes


def load_county_data(data_dir=".", cached_file="county_data.csv", 
                     cached_abridged_file="county_data_abridged.csv",
                     cached=True, abridged=True, infections_data="usafacts", 
                     with_private_data=False, preprocess=True):
    '''  Load in merged county data set
    
    Parameters
    ----------
    data_dir : string; path to the data directory
    
    cached_file : string; name of cached county-level data
    
    cached_abridged_file : string; name of cached abridged county-level data
    
    cached : boolean; whether or not to load in cached data (if possible)
    
    abridged : boolean; whether or not to load in abridged data
    
    infections_data : string; source for daily cases/deaths counts from
                      COVID-19 infections; must be either 'usafacts' or 'nytimes'
                      
    with_private_data : boolean; whether or not to load in private data (if available)
    preprocess: bool
        whether or not to preprocess the features with neighboring data
        
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
        cnty["countyFIPS"] = cnty["countyFIPS"].astype(str).str.zfill(5)
    else: 
        ## ADD PUBLIC DATASETS HERE
        public_datasets = ["ahrf_health", "cdc_svi", "chrr_health", "dhdsp_heart",
                           "dhdsp_stroke", "hpsa_shortage", "ihme_respiratory", "khn_icu",
                           "medicare_chronic", "mit_voting", "nchs_mortality", 
                           "usdss_diabetes", "jhu_interventions", "usda_poverty"]
        ## ADD PRIVATE DATASETS HERE
        private_datasets = ["unacast_mobility", "kinsa_ili", "streetlight_vmt", 
                            "safegraph_socialdistancing", "safegraph_weeklypatterns"]
        
        if with_private_data == True:
            datasets = public_datasets + private_datasets
        else:
            datasets = public_datasets
        
        # load in and clean county-level datasets
        df_ls = []
        cols_ls = []
        for dataset in tqdm(datasets):
            # check if raw data files exist locally; if not, download raw data
            if dataset == "chrr_health":
                os.chdir(oj(data_dir_raw, dataset))
                if not os.path.exists("state_data"):
                    # download raw data
                    os.system("python download.py")
                    print("downloaded " + dataset + " successfully")
                elif len(os.listdir("state_data")) != 51:
                    # download raw data
                    os.system("python download.py")
                    print("downloaded " + dataset + " successfully")        
                os.chdir(orig_dir)
            elif dataset in private_datasets:
                os.chdir(oj(data_dir_raw, dataset))
                if not os.path.exists("../../../../../covid-19-private-data"):
                    # skip loading and cleaning
                    os.chdir(orig_dir)
                    continue
                elif not any(fname.startswith(dataset) \
                             for fname in os.listdir("../../../../../covid-19-private-data")):
                    # skip loading and cleaning
                    os.chdir(orig_dir)
                    continue
                os.chdir(orig_dir)
            else:
                if not any(fname.startswith(dataset) \
                           for fname in os.listdir(oj(data_dir_raw, dataset))):
                    # download raw data
                    os.chdir(oj(data_dir_raw, dataset))
                    os.system("python download.py")
                    print("downloaded " + dataset + " successfully")
                    os.chdir(orig_dir)
                
            # clean data
            os.chdir(oj(data_dir_clean, dataset))
            df = eval("clean_" + dataset + "()")
            df_ls.append(df)
            cols_ls.append(pd.DataFrame({'dataset': dataset, 'feature': df.keys().tolist()}))
            print("loaded and cleaned " + dataset + " successfully")
            os.chdir(orig_dir)
        
        # add wide-format county-level google mobility data
        goog_df = clean_google_mobility(data_dir = oj(data_dir_raw, "google_mobility"), 
                                        out_dir = oj(data_dir_clean, "google_mobility"))
        goog_df = goog_df.loc[goog_df["Region Type"] == "County"][["countyFIPS", "Date", "Sector", "Percent Change"]]
        goog_df = goog_df.pivot_table(index = "countyFIPS", columns = ['Date', 'Sector'], values = 'Percent Change')
        goog_df = pd.DataFrame(goog_df.to_records())
        goog_df.columns = [col.replace("('", "").replace("', '", "_").replace("')", "") for col in goog_df.columns]
        df_ls.append(goog_df)
        cols_ls.append(pd.DataFrame({'dataset': 'google_mobility', 'feature': goog_df.keys().tolist()}))
        print("loaded and cleaned google_mobility successfully")
        
        # save data frame of (datasets, features)
        cols_df = pd.concat(cols_ls, axis=0, sort=False, ignore_index=True)
        cols_df.to_csv("list_of_columns.csv", index=False)
            
        # merge county ids data
        cnty_fips = pd.read_csv(oj(data_dir_raw, "county_ids", "county_fips.csv"))
        cnty_fips["countyFIPS"] = cnty_fips["countyFIPS"].str.zfill(5)
        cnty_latlong = pd.read_csv(oj(data_dir_raw, "county_ids", "county_latlong.csv"))
        cnty_latlong = cnty_latlong[["countyFIPS", "State", "lat", "lon"]]
        cnty_latlong["countyFIPS"] = cnty_latlong["countyFIPS"].astype(str).str.zfill(5)
        cnty_popcenters = pd.read_csv(oj(data_dir_raw, "county_ids", "county_popcenters.csv"))
        cnty_popcenters = cnty_popcenters[["STATEFP", "COUNTYFP", "LATITUDE", "LONGITUDE"]]
        cnty_popcenters = cnty_popcenters.rename(columns = {"LATITUDE": "POP_LATITUDE", 
                                                            "LONGITUDE": "POP_LONGITUDE"})
        cnty_popcenters["countyFIPS"] = cnty_popcenters["STATEFP"].astype(str).str.zfill(2) + cnty_popcenters["COUNTYFP"].astype(str).str.zfill(3)
        cnty = pd.merge(cnty_fips, cnty_latlong, on="countyFIPS", how="left")
        cnty = pd.merge(cnty, cnty_popcenters, on="countyFIPS", how="left")
        
        # merge county-level data with county ids
        for i in range(0, len(df_ls)):
            df_ls[i] = clean_id(df_ls[i])  # remove potentially duplicate ID columns
            df_ls[i] = clean_fips(df_ls[i])  # rename county fips if they have been changed recently
            cnty = pd.merge(cnty, df_ls[i], on='countyFIPS', how="left")  # merge data
            
        # basic preprocessing
        cnty = cnty.loc[:, ~cnty.columns.duplicated()]
        cnty = cnty.infer_objects()
        
        # add new features
        cnty = add_features(cnty)
        
        if abridged == True:
            # get shortlist of important variables for abridged data set
            id_vars = ["countyFIPS", "STATEFP", "COUNTYFP", 'CountyName', 'StateName', 'State', 'lat', 'lon', "POP_LATITUDE", "POP_LONGITUDE"]
            important_vars = id_vars + important_keys(cnty)
            cnty = cnty[important_vars]
            cnty.to_csv(oj(data_dir, cached_abridged_file), header=True, index=False)
            print("saved " + cached_abridged_file + " successfully")
        else:
            # write full county data to file
            cnty.to_csv(oj(data_dir, cached_file), header=True, index=False)
            print("saved " + cached_file + " successfully")
        
    # get cleaned covid-19 infections data
    if infections_data == 'usafacts':
        covid = pd.read_csv(oj(data_dir_clean, "usafacts_infections", "usafacts_infections.csv"))
        covid = clean_fips(covid)
    elif infections_data == 'nytimes':
        covid = pd.read_csv(oj(data_dir_clean, "nytimes_infections", "nytimes_infections.csv"))
        covid = clean_fips(covid)
    
    # add time-series keys
    deaths_keys = [k for k in covid.keys() if '#Deaths' in k]
    cases_keys = [k for k in covid.keys() if '#Cases' in k]
    deaths = covid[deaths_keys].values
    cases = covid[cases_keys].values
    covid['deaths'] = [deaths[i] for i in range(deaths.shape[0])]
    covid['cases'] = [cases[i] for i in range(cases.shape[0])]
    covid['tot_deaths'] = deaths[:, -1]
    covid['tot_cases'] = cases[:, -1]
    covid["countyFIPS"] = covid["countyFIPS"].astype(str).str.zfill(5)
    
    # merge county data with covid data
    df = pd.merge(cnty, covid, on='countyFIPS', how='inner')
    
    # add engineered features
    if preprocess:
        df = add_engineered_features(df, data_dir)
    
    print("loaded and merged COVID-19 cases/deaths data successfully")

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


def clean_fips(df):
    ''' Fix county FIPS which have been recently renamed
    
    Parameters
    ----------
    df : data frame
    
    Returns
    -------
    data frame with most up to date countyFIPS
    '''

    if "02158" in df.countyFIPS.to_list():
        if "02270" in df.countyFIPS.to_list():
            df = df[df.countyFIPS != "02158"]
        else:
            df.countyFIPS[df.countyFIPS == "02158"] = "02270"
    if "46102" in df.countyFIPS.to_list():
        if "46113" in df.countyFIPS.to_list():
            df = df[df.countyFIPS != "46102"]
        else:
            df.countyFIPS[df.countyFIPS == "46102"] == "46113"
    
    return df

def add_engineered_features(df, data_dir):
    '''Add new covid features
    '''

    # add info on neighboring counties
    neighboring_counties_df = pd.read_csv(oj(data_dir, 'county_level/raw/county_ids/county_adjacency2010.csv'))
    neighboring_counties_df['fipscounty'] = neighboring_counties_df['fipscounty'].astype(str).str.zfill(5)
    neighboring_counties_df['fipsneighbor'] = neighboring_counties_df['fipsneighbor'].astype(str).str.zfill(5)
    df['countyFIPS'] = df['countyFIPS'].astype(str).str.zfill(5)
    county_neighbor_deaths = []
    county_neighbor_cases = []
    county_fips = list(df['countyFIPS'])
    for fips in county_fips:
        neighboring_counties = list(neighboring_counties_df.loc[neighboring_counties_df['fipscounty'] == fips]['fipsneighbor'])
        neighboring_county_deaths = list(df.loc[df['countyFIPS'].isin(neighboring_counties)]['deaths'])
        neighboring_county_cases = list(df.loc[df['countyFIPS'].isin(neighboring_counties)]['cases'])
        # if not in county adjacency file, assume neighboring deaths/counts to 0
        if len(neighboring_county_deaths) == 0:  
            n_deaths = len(df.loc[df['countyFIPS'] == fips]['deaths'].iloc[0])
            n_cases = len(df.loc[df['countyFIPS'] == fips]['cases'].iloc[0])
            sum_neighboring_county_deaths = np.zeros(n_deaths)
            sum_neighboring_county_cases = np.zeros(n_cases)
        else:
            sum_neighboring_county_deaths = np.zeros(len(neighboring_county_deaths[0]))
            for deaths in neighboring_county_deaths:
                sum_neighboring_county_deaths += deaths
            sum_neighboring_county_cases = np.zeros(len(neighboring_county_cases[0]))
            for cases in neighboring_county_cases:
                sum_neighboring_county_cases += cases
        county_neighbor_deaths.append(sum_neighboring_county_deaths)
        county_neighbor_cases.append(sum_neighboring_county_cases)
    df['neighbor_deaths'] = county_neighbor_deaths
    df['neighbor_cases'] = county_neighbor_cases
    
    return df
    
def add_features(df):
    '''Add new features
    '''
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
    # geographic variables
    geography = ['CensusRegionName', 'CensusDivisionName',
                 'Rural-UrbanContinuumCode2013']
    
    # demographic variables
    demographics = ['PopulationEstimate2018',
                    'PopTotalMale2017', 'PopTotalFemale2017', 'FracMale2017',
                    'PopulationEstimate65+2017',
                    'PopulationDensityperSqMile2010',
                    'CensusPopulation2010',
                    'MedianAge2010'
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
    social_dist_daily = [var for var in list(df.columns) if "daily_distance_diff" in var]
    interventions = ['stay at home', '>50 gatherings', '>500 gatherings', 'public schools', 'restaurant dine-in', 'entertainment/gym', 'federal guidelines', 'foreign travel ban']
    social = social_dist_daily + interventions
    
    # resource shortages/social vulnerability
    vulnerability = ['SVIPercentile', 'HPSAShortage', 'HPSAServedPop', 'HPSAUnderservedPop']
    
    # neighboring keys

    # get list of important variables
    important_vars = geography + demographics + comorbidity + hospitals + political + age_distr + mortality + social + vulnerability
    
    # keep variables that are in df
    important_vars = [var for var in important_vars if var in list(df.columns)]

    return important_vars


def is_all_data_available(folder, datasets):
    '''
    check if all the subfolders in this folder have the necessary data

    Parameters
    ----------
    folder : str, the folder to check

    datasets: set or list of strs, the set of required data

    Returns
    -------
    is_avail : bool, True or False
    '''
    if type(datasets) is list:
        datasets = set(datasets)
    elif type(datasets) is not set:
        raise ValueError("datasets are of wrong type.")
    for sub_folder in os.walk(folder):
        folder_name = sub_folder[0]
        file_name = folder_name.split("/")[-1]
        if file_name in datasets:
            datasets = datasets - set([file_name])
            if file_name + ".csv" not in sub_folder[2]:
                return False

    return len(datasets) == 0


def load_hospital_data(
        with_private_data=True,
        load_cached_file=True,
        data_dir="./",
        cached_file='hospital_level_data.csv',
        debug=False,
    ):
    '''
    Get the merged hospital level data

    Parameteres
    -----------
    with_private_data : bool, default True
        Whether to combine the private data not posted on github.
    
    load_cached_file : bool, default True
        Whether to load cached file, if false, will try to create a new file.

    cached_file : str, default "hospital_level_data.csv"
        The place to store the cached file

    debug : bool, default False
        Whether to print some logs for debuging.

    Returns
    -------
    out : pandas DataFrame

    Side Effects
    ------------
    If no cached csv file is available, one csv file will be created.
    '''
    hospital_dtype = {
        "CMS Certification Number":str,
        "Hospital Name":str,
        "Hospital Type":str,
        "Street Address":str,
        "City":str,
        "State":str,
        "Zipcode":str,
        "Phone Number":str,
        "Long":np.double,
        "Lat":np.double,
        "Trauma Center Level":np.double,
        "Urban or Rural Designation":str,
        "ICU Beds":int,
        "Total Beds":int,
        "Total Employees":int,
        "ICU Occupancy Rate":np.double,
        "Case Mix Index":np.double,
        "Is Teaching":str,
        "Website":str,
    }

    if load_cached_file:
        if debug:
            print("try to read from cached_file first.")
        try:
            out = pd.read_csv(oj(data_dir, cached_file), index_col=0, dtype=hospital_dtype)
            return out
        except FileNotFoundError as e:
            if debug:
                print("cached file not found. Try to create a new one.")
        except Exception as e:
            print(e)
            raise
    if debug:
        print("Creating a new cached file")
    required_files = [
        'hifld_hospital',
        'cms_cmi',
        'DH_hospital',
        'cms_hospitalpayment',
    ]
    if with_private_data:
        required_files.append('sam_hospital')
    if not is_all_data_available(oj(data_dir, "hospital_level/processed"),required_files):
        print("Not all the cleaned data is available. Halt.")
        return
    if with_private_data:
        base = pd.read_csv(
            oj(data_dir, "hospital_level/processed/sam_hospital/sam_hospital.csv"),
            index_col=0,
            dtype=hospital_dtype,
        )
    else:
        base = pd.read_csv(
            oj(data_dir, "hospital_level/processed/DH_hospital/DH_hospital.csv"),
            index_col=0,
            dtype=hospital_dtype,
        )
    cms_cmi = pd.read_csv(
        oj(data_dir, "hospital_level/processed/cms_cmi/cms_cmi.csv"),
        dtype=hospital_dtype,
    )
    cms_hospitalpayment = pd.read_csv(
        oj(data_dir, "hospital_level/processed/cms_hospitalpayment/cms_hospitalpayment.csv"),
        dtype=hospital_dtype,
    )
    # hifld_hospital = pd.read_csv(
    #     "./hospital_level/processed/hifld_hospital/hifld_hospital.csv",
    #     index_col=0,
    #     dtype=hospital_dtype,
    # )
    del cms_hospitalpayment['Hospital Name']
    base = base.merge(cms_cmi, on="CMS Certification Number", how="outer")
    base = base.merge(cms_hospitalpayment, on="CMS Certification Number", how="outer")
    # new_columns = set(hifld_hospital.columns) - set(base.columns)
    # for col in new_columns:
    #         base[col] = None
    # for ind in base.index:
    #     rows = hifld_hospital[hifld_hospital['Zipcode'] == base.loc[ind, 'Zipcode']]
    #     if len(rows) == 1:
    #         base.loc[rows.index[0], new_columns] = rows.iloc[0][new_columns]
    #     elif len(rows) > 1:
    #         argmin = np.argmin([distance(
    #             rows.loc[i, 'Lat'],
    #             base.loc[ind, 'Lat'],
    #             rows.loc[i, 'Long'],
    #             base.loc[ind, 'Long']
    #         ) for i in rows.index])
    #         matched_index = rows.index[argmin]
    #         base.loc[matched_index, new_columns] = rows.loc[matched_index, new_columns]
    base.to_csv(oj(data_dir, cached_file))
    return base

def distance(lat1, lat2, lon1, lon2): 
      
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371
       
    # calculate the result 
    return(c * r) 


def load_nursinghome_data(data_dir=".", cached_file="nursinghomes_data.csv", cached=True):
    '''  Load in merged nursing homes data set
    
    Parameters
    ----------
    data_dir : string; path to the data directory
    
    cached_file : string; name of cached nursing homes-level data
    
    cached : boolean; whether or not to load in cached data (if possible)
        
    Returns
    -------
    data frame with fully merged nursing homes-level data set
    '''    
    # data directories
    orig_dir = os.getcwd()
    data_dir_raw = oj(data_dir, "nursinghome_level", "raw")
    data_dir_clean = oj(data_dir, "nursinghome_level", "processed")
    
    if cached == True:  
        # read in cached data
        if os.path.exists(oj(data_dir, cached_file)):
            nh = pd.read_csv(oj(data_dir, cached_file))
        else:
            raise ValueError("Cached file cannot be found. " + "Please set cached = False")
    else: 
        
        ## ADD PUBLIC DATASETS HERE
        datasets = ["nyt_nursinghomes", "hifld_nursinghomes"]
        
        # load in and clean county-level datasets
        df_ls = []
        for dataset in tqdm(datasets):
            # check if raw data files exist locally; if not, download raw data
            if not any(fname.startswith(dataset) \
                       for fname in os.listdir(oj(data_dir_raw, dataset))):
                # download raw data
                os.chdir(oj(data_dir_raw, dataset))
                os.system("python download.py")
                print("downloaded " + dataset + " successfully")
                os.chdir(orig_dir)
                
            # clean data
            os.chdir(oj(data_dir_clean, dataset))
            df = eval("clean_" + dataset + "()")
            df_ls.append(df)
            print("loaded and cleaned " + dataset + " successfully")
            os.chdir(orig_dir)

        # merge nursing homes data
        manual_merge_tab = pd.read_csv(oj(data_dir, "nursinghome_level", "manual_merge_table.csv"))
        nh = merge_nursinghome_data(df_ls[0], df_ls[1], manual_merge_tab)
        print("merged nursing homes data successfully")
        
        # write full county data to file
        nh.to_csv(oj(data_dir, cached_file), index=False)
        print("saved " + cached_file + " successfully")

    # ensure consistent data types
    nh["countyFIPS"] = nh["countyFIPS"].astype(str).str.zfill(5)
    
    return nh


def merge_nursinghome_data(nyt, hifld, manual_merge_tab):
    ''' merge nursing home data
    
    Parameters
    ----------
    nyt : cleaned nyt nursing homes data
    
    hifld : cleaned hifld nursing homes data
    
    manual_merge_tab : merge table with merges to manually correct
        
    Returns
    -------
    data frame with merged nursing homes data
    '''  
    
    try:
        from fuzzywuzzy import process, fuzz
    except ImportError:
        sys.exit("""You need fuzzywuzzy.
                    Install it from https://pypi.org/project/fuzzywuzzy/
                    or run pip install fuzzywuzzy.""")
    
    # clean names and cities for better merge
    nyt = clean_nh_cities(nyt)
    nyt = clean_nh_names(nyt, level = 1)
    nyt2 = clean_nh_names(copy.deepcopy(nyt), level = 2)  # more ambitious cleaning
    hifld = clean_nh_cities(hifld)
    hifld = clean_nh_names(hifld, level = 1)
    hifld2 = clean_nh_names(copy.deepcopy(hifld), level = 2)  # more ambitious cleaning
    
    # fuzzy merging
    matched_fid = []
    for i in range(nyt.shape[0]):
        name = nyt.loc[i, "Name"]
        name2 = nyt2.loc[i, "Name"]
        city = nyt.loc[i, "City"]
        state = nyt.loc[i, "State"]

        # get exact matches
        matched_all = hifld.loc[(hifld["Name"] == name) &\
                                (hifld["City"] == city) &\
                                (hifld["State"] == state)]

        if matched_all.shape[0] == 1:  # one exact match
            fid = matched_all.iloc[0]["Fid"]
        elif matched_all.shape[0] > 1:  # more than one exact match
            if matched_all.Name.iloc[0] == "CHRISTIAN HEALTH CARE CENTER":
                fid = 6658  # manual merge
            else:
                print("Multiple exact matches for: " + name)
        else:  # if no exact match, do fuzzy matching
            # first try exact matching on city and state
            hifld_matched = hifld.loc[(hifld["City"] == city) & (hifld["State"] == state)]
            if hifld_matched.shape[0] > 0:
                matched = process.extractOne(name, hifld_matched["Name"], scorer=fuzz.WRatio)
                if matched[1] >= 87:  # if meet threshold requirement, found match
                    matched_fids = hifld_matched.loc[hifld_matched["Name"] == matched[0]]
                else:  # try using names that are even more abbreviated/cleaned
                    hifld2_matched = hifld2.loc[(hifld2["City"] == city) & (hifld2["State"] == state)] 
                    matched = process.extractOne(name2, hifld2_matched["Name"], scorer=fuzz.WRatio)
                    if matched[1] >= 87:  # if meet threshold requirement, found match
                        matched_fids = hifld2_matched.loc[hifld2_matched["Name"] == matched[0]]
                    else:  # finally try using different distance metric
                        matched = process.extractOne(name2, hifld2_matched["Name"], scorer=fuzz.ratio)
                        matched_fids = hifld2_matched.loc[hifld2_matched["Name"] == matched[0]]

                # get (a single) matched FID
                if matched_fids.shape[0] == 1:
                    fid = matched_fids["Fid"].iloc[0]
                else:  # if multiple matched FIDs
                    if not matched_fids["Population"].isna().all() == 0:  # not all nans in pop field
                        # choose one with large population
                        fid = matched_fids.loc[matched_fids["Population"] ==\
                                               np.nanmax(matched_fids["Population"])]["Fid"].iloc[0]
                    else:  # all nans in population field
                        fid = matched_fids["Fid"].iloc[0]  # take first one
            else:  # do manual merge later
                fid = np.NaN
        matched_fid.append(fid)
    nyt["Matched FID"] = matched_fid
            
    # fix some nursing home matched FIDs manually
    for i in range(manual_merge_tab.shape[0]):
        name = manual_merge_tab.Name.iloc[i]
        fid = manual_merge_tab.FID.iloc[i]
        city = manual_merge_tab.City.iloc[i]
        state = manual_merge_tab.State.iloc[i]
        idx = (nyt.Name == name) & (nyt.City == city) & (nyt.State == state)
        nyt["Matched FID"].loc[idx] = fid
    
    # take entry with max #cases to deal with duplicates in nyt
    nyt_duplicated_ls = []
    for fid in nyt["Matched FID"].loc[nyt["Matched FID"].duplicated()].unique():
        if fid == -999:
            continue
        nyt_duplicated = nyt.loc[nyt["Matched FID"] == fid]
        nyt_duplicated = nyt_duplicated.loc[nyt_duplicated["Cases_2020-05-11"] ==\
                                            np.max(nyt_duplicated["Cases_2020-05-11"])]
        nyt_duplicated_ls.append(nyt_duplicated)
        nyt = nyt.loc[nyt["Matched FID"] != fid]
    nyt_duplicated = pd.concat(nyt_duplicated_ls, axis = 0, sort = False)
    nyt = pd.concat([nyt, nyt_duplicated], axis = 0, sort = False)

    #nyt.to_csv("full_merge_table.csv", index=False)
    
    # merge with hifld
    nyt["Matched FID"] = nyt["Matched FID"].astype(int)
    nyt = nyt.rename(columns = {"Name": "NYT Name", "City": "NYT City", "State": "NYT State"})
    nh = pd.merge(hifld, nyt, left_on = "Fid", right_on = "Matched FID", how = "right")
    nh = nh.replace(-999, np.NaN)

    return nh
    
            
def clean_nh_names(df, level = 1):
    ''' clean nursing home names (helper function for merge_nursinghome_data())
    
    Parameters
    ----------
    df : data frame to clean
    
    level : denotes how much cleaning to do; 1 = minimal, 2 = more
        
    Returns
    -------
    data frame with cleaned nursing home names
    '''    
    
    rm_words = [".", ",", " LTD", " LLC", " INC", "'"]
    for word in rm_words:
        df.Name = df.Name.str.replace(word, "")
    df.Name = df.Name.str.replace("&", "AND")
    df.Name = df.Name.str.replace("HEALTHCARE", "HEALTH CARE")
    df.Name = df.Name.str.replace("REHABILITATION", "REHAB")
    
    if level > 1:  # more ambitious cleaning
        rm_words = ["REHAB", "CENTER", "CENTRE", "FACILITY", "NURSING HOME", "CONVALESCENT",
                    "NURSING", "WELLNESS SUITES", "RETIREMENT COMMUNITY", "HEALTH", "SENIOR",
                    "LIVING", "AND"]  
        for word in rm_words:
            df.Name = df.Name.str.replace(word, "")
    
    # remove extra spaces
    df.Name = df.Name.apply(lambda x: re.sub(' +', ' ', x))  
    df.Name = df.Name.str.strip()
    return df

def clean_nh_cities(df):
    ''' clean nursing home city names (helper function for merge_nursinghome_data())
    
    Parameters
    ----------
    df : data frame to clean
        
    Returns
    -------
    data frame with cleaned nursing home city names
    '''  
    df.City = df.City.str.replace(",", "")
    df.City = df.City.str.replace(".", "")
    df.City = df.City.str.replace("SAINT", "ST")
    df.City = df.City.str.replace("MOUNT ", "MT ")
    df.City = df.City.str.replace("TOWNSHIP", "")
    df.City = df.City.str.replace("'", "")
    #df.City = df.City.str.replace("CITY", "")
    df.City = df.City.str.strip()
    return df


def load_socialmobility_data(data_dir=".", level="country", df_shape="long"):
    '''  Load in merged social mobility data set
    
    Parameters
    ----------
    data_dir : string; path to the data directory
    
    level : one of {"country", "county", "state", "state/province", "city"}; level of granularity of 
            social mobility data; "state/province" (which will include states/provinces from all countries) 
            has not been implemented yet
        
    df_shape : one of {"long", "wide"}; whether to return long or wide data frame
        
    Returns
    -------
    data frame with merged and cleaned social mobility data set; 
        for details on the data columns, see the readmes for the apple mobility and google mobility data at 
        data/county_level/processed/apple_mobility and data/county_level/processed/google_mobility respectively
    ''' 
    
    # data directories
    orig_dir = os.getcwd()
    data_dir_raw = oj(data_dir, "county_level", "raw")
    data_dir_clean = oj(data_dir, "county_level", "processed")
    
    # load and clean most up-to-date apple mobility data
    appl_df = clean_apple_mobility(data_dir = oj(data_dir_raw, "apple_mobility"), 
                                   out_dir = oj(data_dir_clean, "apple_mobility"))
    appl_df["Dataset"] = "apple"
    print("loaded and cleaned apple mobility data successfully")
    goog_df = clean_google_mobility(data_dir = oj(data_dir_raw, "google_mobility"), 
                                    out_dir = oj(data_dir_clean, "google_mobility"))
    goog_df["Dataset"] = "google"
    print("loaded and cleaned google mobility data successfully")
    
    if level == "country":  # get country-level data
        appl_df = appl_df.loc[appl_df["Region Type"] == "Country"]
        appl_df = appl_df.drop(columns = ["Region Type"])
        appl_df = appl_df.rename(columns = {"Region": "Country"})
        
        goog_df = goog_df.loc[goog_df["Region Type"] == "Country"]
        goog_df = goog_df.drop(columns = ["Region Type", "State/Province", "County", "countyFIPS"])
        
        df = pd.concat([appl_df, goog_df], axis = 0, sort = False)
        
    elif level == "state":  # get US state-level data
        us_states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
                     "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
                     "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
                     "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
                     "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
                     "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
                     "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
        appl_df = appl_df.loc[(appl_df["Region Type"] == "State/Province") & (appl_df["Region"].isin(us_states))]
        appl_df = appl_df.drop(columns = ["Region Type"])
        appl_df = appl_df.rename(columns = {"Region": "State"})
        
        goog_df = goog_df.loc[(goog_df["Region Type"] == "State/Province") &\
                              (goog_df["State/Province"].isin(us_states))]
        goog_df = goog_df.drop(columns = ["Region Type", "Country", "County", "countyFIPS"])
        goog_df = goog_df.rename(columns = {"State/Province": "State"})
        
        df = pd.concat([appl_df, goog_df], axis = 0, sort = False)
    
    elif level == "state/province":  # get world state/province level data
        print("level == 'state/province' has not been implemented yet. Need to check if names of provinces in apple and google data sets overlap/match")
        return
    
    elif level == "county":  # get US county level data
        goog_df = goog_df.loc[goog_df["Region Type"] == "County"]
        goog_df = goog_df.drop(columns = ["Region Type", "Country"])
        goog_df = goog_df.rename(columns = {"State/Province": "State"})
        df = goog_df
        
    elif level == "city":
        appl_df = appl_df.loc[appl_df["Region Type"] == "City"]
        appl_df = appl_df.drop(columns = ["Region Type"])
        appl_df = appl_df.rename(columns = {"Region": "City"})
        df = appl_df
    
    if df_shape == "wide":
        keys = [col for col in df.columns if col not in ['Date', 'Sector', 'Dataset', 'Percent Change']]
        df = df.pivot_table(index = keys, columns = ['Date', 'Sector', 'Dataset'], values = 'Percent Change')
        #df = pd.DataFrame(df.to_records())
        #df.columns = [col.replace("('", "").replace("', '", "").replace("')", "") \
        #              for col in df.columns]
    
    return df
