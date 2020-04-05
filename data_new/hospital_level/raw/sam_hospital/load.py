#!/usr/bin/python3

import pandas as pd

def load_sam_hospital(input="./sam_hospital.csv"):
    raw = pd.read_csv(input)
    return raw

if __name__ == '__main__':
    load_sam_hospital()
    print("load sam_hospital successfully.")

