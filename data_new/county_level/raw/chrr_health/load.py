#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_chrr_health(data_dir='.'):
    ''' Load in County Health Rankings & Roadmaps data (2020)
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing 
               ./state_data/chrr_health_STATENAME.XLSX
    
    Returns
    -------
    data frame
    '''
    
    states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
              'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 
              'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 
              'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 
              'Nebraska', 'Nevada', 'New%20Hampshire', 'New%20Jersey', 'New%20Mexico', 
              'New%20York', 'North%20Carolina', 'North%20Dakota', 'Ohio', 'Oklahoma', 'Oregon', 
              'Pennsylvania', 'Rhode%20Island', 'South%20Carolina', 'South%20Dakota', 
              'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
              'West%20Virginia', 'Wisconsin', 'Wyoming', 'District%20of%20Columbia']
    raw_ls = []
    for state in states:
        raw = pd.read_excel(oj(data_dir, 'state_data', 'chrr_health_' + state + '.xlsx'), 
                           sheet_name = 'Ranked Measure Data', 
                           skiprows = 1)
        keep_cols = ['FIPS', 'Years of Potential Life Lost Rate', '% Fair or Poor Health', 
                     'Average Number of Physically Unhealthy Days', 
                     'Average Number of Mentally Unhealthy Days', 
                     '% Low Birthweight', '% Smokers', '% Adults with Obesity', 
                     'Food Environment Index', '% Physically Inactive', 
                     '% With Access to Exercise Opportunities', '% Excessive Drinking', 
                     '% Driving Deaths with Alcohol Involvement', 'Chlamydia Rate', 
                     'Teen Birth Rate', '% Uninsured', 'Primary Care Physicians Ratio', 
                     'Dentist Ratio', 'Mental Health Provider Ratio', 
                     'Preventable Hospitalization Rate', '% With Annual Mammogram', 
                     '% Vaccinated', 'High School Graduation Rate', '% Some College', 
                     '% Unemployed', '% Children in Poverty', 'Income Ratio',
                     '% Single-Parent Households', 'Social Association Rate', 
                     'Violent Crime Rate', 'Injury Death Rate', 'Average Daily PM2.5', 
                     'Presence of Water Violation', '% Severe Housing Problems', 
                     '% Drive Alone to Work', '% Long Commute - Drives Alone']
        raw_ls.append(raw[keep_cols])
    raw = pd.concat(raw_ls)
    
    return raw

if __name__ == '__main__':
    raw = load_chrr_health()
    print('loaded chrr_health successfully.')

