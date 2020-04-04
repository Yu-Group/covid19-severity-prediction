#!/usr/bin/python3

import pandas as pd

def load_DH_hospital(input="./DH_hospital.csv"):
    raw = pd.read_csv(input)
    return raw

if __name__ == '__main__':
    raw = load_DH_hospital()
    print('load DH_hospital successfully.')
