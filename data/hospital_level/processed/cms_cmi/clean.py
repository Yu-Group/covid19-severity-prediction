#! /usr/bin/python3

import pandas as pd
import sys
sys.path.append("../../raw/cms_cmi")
from load import load_cms_cmi

def clean_cms_cmi(input="../../raw/cms_cmi/cms_cmi.xlsx"):
    raw = load_cms_cmi(input)
    raw.columns = (
        ['CMS Certification Number', 'Case Mix Index'] 
        + list(raw.columns[2:])
    )
    raw.to_csv("cms_cmi.csv", index=False)
    return raw

if __name__ == '__main__':
    clean_cms_cmi()
    print("clean cms_cmi successfully.")

