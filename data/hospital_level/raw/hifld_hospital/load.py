#!/usr/bin/python3

import pandas as pd

def load_hifld_hospital(input="../../raw/hifld_hospital/hifld_hospital.csv"):
    raw = pd.read_csv(input)
    return raw

if __name__ == '__main__':
    raw = load_hifld_hospital()
    print('load hifld_hospital successfully.')
