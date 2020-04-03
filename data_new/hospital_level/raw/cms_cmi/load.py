#!/usr/bin/python3

import pandas as pd

def load_cms_cmi(input="./cms_cmi.xlsx"):
    raw = pd.read_excel(input)
    raw["Provider No."] = raw["Provider No."].astype(str).apply(
        lambda x : x.zfill(6),
    )
    return raw

if __name__ == '__main__':
    load_cms_cmi()
    print("load cms_cmi successfully.")

