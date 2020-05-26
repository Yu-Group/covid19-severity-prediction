#! /usr/bin/python3

import pandas as pd
import sys
sys.path.append("../../raw/DH_hospital")
from load import load_DH_hospital

def clean_DH_hospital(input="../../raw/DH_hospital/DH_hospital.csv"):
    raw = load_DH_hospital(input)
    raw = raw.rename(columns={
        "Facility ID": "CMS Certification Number",
        "Facility Name": "Hospital Name",
    })
    raw.to_csv("DH_hospital.csv", index=False)
    return raw

if __name__ == '__main__':
    clean_DH_hospital()
    print("clean DH_hospital successfully.")
