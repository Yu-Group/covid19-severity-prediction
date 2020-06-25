#! /usr/bin/python3

import pandas as pd
import sys
sys.path.append("../../raw/DH_hospital")
from load import load_DH_hospital

def clean_DH_hospital(input="../../raw/DH_hospital/DH_hospital.csv"):
    raw = load_DH_hospital(input)
    raw = raw.rename(columns={
            "X" : "lat",
            "Y" : "long",
            "HOSPITAL_TYPE" : "Hospital type",
            "HOSPITAL_NAME" : "Hospital name",
            "NUM_ICU_BEDS" : "Number of ICU Beds",
            "NUM_LICENSED_BEDS" : "Number of Licensed Beds",
            "NUM_STAFFED_BEDS" : "Number of Staffed Beds",
            "CNTY_FIPS" : "CountyFIPS",
            "BED_UTILIZATION": "Bed utilization rate",
    })
    raw.to_csv("DH_hospital.csv", index=False)
    return raw

if __name__ == '__main__':
    clean_DH_hospital()
    print("clean DH_hospital successfully.")
