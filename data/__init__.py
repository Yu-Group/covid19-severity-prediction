#!/usr/bin/python3

import numpy as np
import pandas as pd
import os
from os.path import join as oj
import sys
from math import radians, sin, cos, sqrt, asin
from sklearn.neighbors import NearestNeighbors
#from hospital_level.processed.cms_cmi.clean import clean_cms_cmi
#from hospital_level.processed.cms_hospitalpayment.clean import clean_cms_hospitalpayment

from .county_level.processed.usafacts_infections.clean import clean_usafacts_infections
from .county_level.processed.nytimes_infections.clean import clean_nytimes_infections
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
        cnty["countyFIPS"] = cnty["countyFIPS"].astype(str).str.zfill(5)
    else: 
        ## ADD PUBLIC DATASETS HERE
        public_datasets = ["ahrf_health", "cdc_svi", "chrr_health", "dhdsp_heart",
                           "dhdsp_stroke", "hpsa_shortage", "ihme_respiratory", "khn_icu",
                           "medicare_chronic", "mit_voting", "nchs_mortality", 
                           "usdss_diabetes", "jhu_interventions"]
        ## ADD PRIVATE DATASETS HERE
        private_datasets = ["unacast_mobility", "kinsa_ili", "streetlight_vmt"]
        
        # load in and clean county-level datasets
        df_ls = []
        for dataset in public_datasets + private_datasets:
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
                os.chdir(orig_dir)
            elif dataset != "jhu_interventions":
                if not any(fname.startswith(dataset) \
                           for fname in os.listdir(oj(data_dir_raw, dataset))):
                    # download raw data
                    os.chdir(oj(data_dir_raw, dataset))
                    os.system("python download.py")
                    print("downloaded " + dataset + " successfully")
                    os.chdir(orig_dir)
                
            # clean data
            os.chdir(oj(data_dir_clean, dataset))
            df_ls.append(eval("clean_" + dataset + "()"))
            print("loaded and cleaned " + dataset + " successfully")
            os.chdir(orig_dir)
            
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
        
    # get covid-19 infections data
    if infections_data == 'usafacts':
        os.chdir(oj(data_dir_raw, "usafacts_infections"))
        os.system("python download.py")
        print("downloaded usafacts_infections successfully")
        os.chdir(orig_dir)
        covid = clean_usafacts_infections(oj(data_dir_raw, "usafacts_infections"), 
                                          oj(data_dir_clean, "usafacts_infections"))
    elif infections_data == 'nytimes':
        os.chdir(oj(data_dir_raw, "nytimes_infections"))
        os.system("python download.py")
        print("downloaded nytimes_infections successfully")
        os.chdir(orig_dir)
        covid = clean_nytimes_infections(oj(data_dir_raw, "nytimes_infections"), 
                                         oj(data_dir_clean, "nytimes_infections"))
    
    # add time-series keys
    deaths_keys = [k for k in covid.keys() if '#Deaths' in k]
    cases_keys = [k for k in covid.keys() if '#Cases' in k]
    deaths = covid[deaths_keys].values
    cases = covid[cases_keys].values
    covid['deaths'] = [deaths[i] for i in range(deaths.shape[0])]
    covid['cases'] = [cases[i] for i in range(cases.shape[0])]
    covid['tot_deaths'] = deaths[:, -1]
    covid['tot_cases'] = cases[:, -1]
    
    # merge county data with covid data
    if rm_na == True:
        df = pd.merge(cnty, covid, on='countyFIPS', how='right')
    else:
        df = pd.merge(cnty, covid, on='countyFIPS', how='left')

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
    social_dist_daily = [var for var in list(df.columns) if "daily_distance_diff" in var]
    interventions = ['stay at home', '>50 gatherings', '>500 gatherings', 'public schools', 'restaurant dine-in', 'entertainment/gym', 'federal guidelines', 'foreign travel ban']
    social = social_dist_daily + interventions
    
    # resource shortages/social vulnerability
    vulnerability = ['SVIPercentile', 'HPSAShortage', 'HPSAServedPop', 'HPSAUnderservedPop']

    # get list of important variables
    important_vars = demographics + comorbidity + hospitals + political + age_distr + mortality + social
    
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


def load_hospital_level_data(
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
        index_col=0,
        dtype=hospital_dtype,
    )
    cms_hospitalpayment = pd.read_csv(
        oj(data_dir, "hospital_level/processed/cms_hospitalpayment/cms_hospitalpayment.csv"),
        index_col=0,
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
