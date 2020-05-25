import numpy as np
import pandas as pd
from os.path import join as oj

# TODO: confirm these changes don't affect other areas of the code
def merge_county_and_hosp(df_county, df_hospital):
    outcomes = ['tot_cases', 'tot_deaths']
    # df_hospital = df_hospital.loc[~df_hospital.countyFIPS.isna()]
    # df_hospital['countyFIPS'] = df_hospital['countyFIPS'].astype(int).astype(str).str.zfill(5)
    df_hospital['countyFIPS'][~df_hospital.countyFIPS.isna()] = df_hospital['countyFIPS'][~df_hospital.countyFIPS.isna()].astype(int).astype(str).str.zfill(5)
    df = df_hospital.merge(df_county, how='left', on='countyFIPS')
    df[outcomes] = df[outcomes].fillna(0)

    # aggregate employees by county
    total_emp_county = df.groupby('countyFIPS').agg({'Hospital Employees': 'sum'})
    total_emp_county = total_emp_county.rename(columns={'Hospital Employees': 'Hospital Employees in County'})
    df_county = pd.merge(df_county, total_emp_county, how='left', on='countyFIPS')
    df = pd.merge(df, total_emp_county, how='left', on='countyFIPS')

    # filter hospitals
    # df = df[~df['countyFIPS'].isna()] # & df['IsAcademicHospital'] & df['Hospital Employees'] > 0]
    df = df.sort_values(by=['tot_deaths', 'Hospital Employees'], ascending=False)
    df = df.drop(columns='Hospital Name')
    df = df.rename(columns={'Facility Name': 'Hospital Name'})
    df = df.drop_duplicates('CMS Certification Number', keep=False)

    # fraction of employees out of all county hospitals
    df['Frac Hospital Employees of County'] = df['Hospital Employees'] / df['Hospital Employees in County']
    df = df.loc[:,~df.columns.duplicated()]
    return df
