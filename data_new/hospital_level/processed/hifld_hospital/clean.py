#! /usr/bin/python3

import pandas as pd
import sys
import string
sys.path.append("../../raw/hifld_hospital")
from load import load_hifld_hospital

def clean_hifld_hospital(input="../../raw/hifld_hospital/hifld_hospital.csv"):
    raw = load_hifld_hospital(input)
    # only get the hospital with status open
    raw = raw[raw['STATUS'] == 'OPEN']
    cleaned = pd.DataFrame(index=raw.index)
    # change the column names 
    cleaned['Hospital Name'] = raw['NAME'].str.lower()
    cleaned['Long'] = raw['LONGITUDE']
    cleaned['Lat'] = raw['LATITUDE']
    cleaned['Address'] = raw['ADDRESS'].str.lower()
    cleaned['City'] = raw['CITY'].str.lower()
    cleaned['Zipcode'] = raw['ZIP']
    cleaned['State'] = raw['STATE'].str.upper()
    cleaned['Telephone'] = raw['TELEPHONE']
    cleaned['countyFIPS'] = raw['COUNTYFIPS']
    cleaned['Total Beds'] = raw['BEDS']

    # deal with websites
    cleaned['Website'] = raw['WEBSITE']
    for i in cleaned.index:
        website = cleaned.loc[i, 'Website'].lower().replace(" ","")
        if website == "":
            website = ""
        elif "https://" == website[:8]:
            website = website[8:]
        elif "http://" == website[:7]:
            website = website[7:]
        if website[-1] == '/':
            website = website[:-1]
        cleaned.loc[i,'Website'] = website
    
    # deal with trauma center
    cleaned['Trauma Center Level'] = raw['TRAUMA']
    for i in cleaned.index:
        trauma = cleaned.loc[i, 'Trauma Center Level']
        if trauma == "NOT AVAILABLE":
            trauma = ""
        elif trauma == 'LEVEL V':
            trauma = "5"
        elif trauma == 'LEVEL IV':
            trauma = "4"
        elif trauma == 'LEVEL III':
            trauma = '3'
        elif trauma == 'LEVEL II':
            trauma = "2"
        elif trauma == 'LEVEL I':
            trauma = "1"
        else:
            trauma = ""
        cleaned.loc[i,'Trauma Center Level'] = trauma
    
    cleaned['Hospital Type'] = raw['TYPE'].str.lower()
    cleaned.to_csv("hifld_hospital.csv", index=False, header=True)
    return cleaned

if __name__ == '__main__':
    clean_hifld_hospital()
    print("clean hifld successfully.")
