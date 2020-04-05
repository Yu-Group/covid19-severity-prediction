#!/usr/bin/python3

import pandas as pd

def load_cms_hospitalpayment(input="./cms_hospitalpayment.xlsx"):
    teaching = pd.read_excel(
        input,
        index_col=0,
        dtype=str,
    )
    return teaching

if __name__ == '__main__':
    load_cms_hospitalpayment()
    print("load cms_hospitalpayment successfully.")

