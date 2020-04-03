#! /usr/bin/python3

import pandas as pd
import sys
sys.path.append("../../raw/hifld_hospital")
from load import load_hifld_hospital

def clean_hifld_hospital(input="../../raw/hifld_hospital/hifld_hospital.csv"):
    raw = load_hifld_hospital(input)
    cleaned = pd.DataFrame(index=raw.index)
    # change the column names 
    cleaned['Long'] = raw['LONGITUDE']
    cleaned['Lat'] = raw['LATITUDE']
    cleaned['Hospital Name'] = raw['NAME']
    cleaned['Address'] = raw['ADDRESS']
    cleaned['City'] = raw['CITY']
    cleaned['Zipcode'] = raw['ZIP']
    cleaned['State'] = raw['STATE']
    cleaned['Telephone'] = raw['TELEPHONE']
    cleaned['Status'] = raw['STATUS']
    cleaned['countyFIPS'] = raw['COUNTYFIPS']
    cleaned['Total Beds'] = raw['BEDS']
    cleaned['Website'] = raw['WEBSITE']
    cleaned['Trauma Center Level'] = raw['TRAUMA']
    cleaned['Hospital Type'] = raw['TYPE']
    cleaned.to_csv("hifld_hospital.csv", index=False, header=True)
    return cleaned

if __name__ == '__main__':
    clean_hifld_hospital()
    print("clean hifld successfully.")
