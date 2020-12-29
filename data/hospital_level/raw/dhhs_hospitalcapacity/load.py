#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os
from bs4 import BeautifulSoup
import urllib
import re

def load_dhhs_hospitalcapacity(data_dir='.'):
    ''' Load in Dept of Health and Human Services COVID-19 Reported Patient 
    Impact and Hospital Capacity by Facility
    
    Parameters
    ----------
    data_dir : str; path to the data directory to write dhhs_hospitalcapacity.csv
    
    Returns
    -------
    data frame
    '''
    
    # download data from source, which is updated daily
    html_page = urllib.request.urlopen("https://healthdata.gov/dataset/covid-19-reported-patient-impact-and-hospital-capacity-facility")
    soup = BeautifulSoup(html_page)
    for link in soup.findAll('a'):
        if link.get('href') is None:
            next
        elif 'reported_hospital_capacity_admissions_facility_level_weekly_average_timeseries' in link.get('href'):
            fname = link.get('href')
            break
    
    # load in data
    raw = pd.read_csv(fname, na_values=[-999999])
    raw.to_csv(oj(data_dir, "dhhs_hospitalcapacity.csv"), header=True, index=False)
    
    return raw

if __name__ == '__main__':
    raw = load_dhhs_hospitalcapacity()
    print('loaded dhhs_hospitalcapacity successfully.')



