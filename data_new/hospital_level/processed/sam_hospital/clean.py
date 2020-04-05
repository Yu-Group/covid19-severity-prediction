#!/usr/bin/python3

import pandas as pd
import sys
sys.path.append("../../raw/sam_hospital/")
from load import load_sam_hospital

def clean_sam_hospital(input="../../raw/sam_hospital/sam_hospital.csv"):
    raw = load_sam_hospital(input)
    clean = pd.DataFrame(index=raw.index)
    clean['CMS Certification Number'] = raw['CMS Certification Number']
    clean['Hospital Name'] = raw['Facility Name'].str.lower()
    clean['Street Address'] = raw['Street Address'].str.lower()
    clean['City'] = raw['City'].str.lower()
    clean['Zipcode'] = raw['ZIP']
    clean['State'] = raw['State'].str.upper()
    clean['Hospital Type'] = raw['Type of Facility'].str.lower()
    clean['Total Employees'] = raw['Total Employees']
    clean['Urban or Rural Designation'] = raw['Urban or Rural Designation'].str.lower()
    clean['Lat'] = raw['Latitude']
    clean['Long'] = raw['Longitude']
    clean['Total Beds'] = raw['Total Beds']
    clean['ICU Beds'] = (
        raw['ICU Beds']
   #     + raw['Coronary ICU Beds'] 
   #     + raw['Surgical ICU Beds']
   #     + raw['Psych ICU Beds']
   #     + raw['Pediatric ICU Beds']
   #     + raw['Trauma ICU Beds']
   #     + raw['Neonatal ICU Beds']
   #     + raw['Detox ICU Beds']
   #     + raw['Premature ICU Beds']
    )
    clean['ICU Occupancy Rate'] = raw['ICU Occupancy Rate']
    clean.to_csv("sam_hospital.csv",index=False)
    return clean

if __name__ == '__main__':
    clean_sam_hospital()
    print("clean sam_hospital successfully.")

