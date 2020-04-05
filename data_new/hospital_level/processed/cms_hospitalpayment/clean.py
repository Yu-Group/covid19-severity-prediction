#! /usr/bin/python3

import pandas as pd
import sys
sys.path.append("../../raw/cms_hospitalpayment")
from load import load_cms_hospitalpayment

def clean_cms_hospitalpayment(input="../../raw/cms_hospitalpayment/cms_hospitalpayment.xlsx"):
    raw = load_cms_hospitalpayment(input)
    cleaned = pd.DataFrame(index=raw.index)
    cleaned['CMS Certification Number'] = raw['CCN'].str.zfill(6)
    cleaned['Hospital Name'] = raw['Hospital Name'].str.lower()
    cleaned['TIN'] = raw['TIN']
    cleaned.to_csv("cms_hospitalpayment.csv", index=False)
    return raw

if __name__ == '__main__':
    clean_cms_hospitalpayment()
    print("clean cms_hospitalpayment successfully.")

