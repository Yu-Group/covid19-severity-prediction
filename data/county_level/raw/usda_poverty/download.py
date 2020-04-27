#! /usr/bin/python3
import pandas as pd
import os


# download raw data files
os.system("wget https://www.ers.usda.gov/webdocs/DataFiles/48747/PovertyEstimates.xls -O usda_poverty.xls")



# generate meta_data.csv
if not os.path.exists("./DOC/meta_data.csv"):
    if not os.path.exists("DOC"):
        os.mkdir("DOC")
    pov_col_desc = pd.read_excel("usda_poverty.xls", sheet_name="Variable Descriptions")
    pov_col_desc.to_csv("./DOC/meta_data.csv")