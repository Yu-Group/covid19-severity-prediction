#! /usr/bin/python3
# this will change daily, check here: https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/ (updates around 9am)
# date is the date retrieved (includes cases up to but not including that day)
import os
import numpy as np
import pandas as pd
import sys

data_dir = "./"
os.system("wget https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv -O {}confirmed_cases.csv".format(data_dir))
os.system("wget https://static.usafacts.org/public/data/covid-19/covid_deaths_usafacts.csv -O {}deaths.csv".format(data_dir))



for tag in ['confirmed_cases', 'deaths']:
    path = "{}/{}.csv".format(data_dir, tag)
    out_path = "{}/{}.csv".format(data_dir, tag)

    # load data
    raw = pd.read_csv(path, encoding="utf-8", dtype={'countyFIPS':str})

    # remove unnamed cols
    for col in raw.columns:
        if 'Unnamed' in col:
            del raw[col]


    # preprocess get all the duplicates
    replicates = raw.groupby(['countyFIPS', 'stateFIPS'])['County Name'].count().reset_index()

    # preprocess merge rows with the same (county, state) pair by adding up the other numbers
    cleaned = raw.groupby(['countyFIPS', 'County Name', 'State', 'stateFIPS']).sum().reset_index()

    # save the cleaned data
    cleaned.T.to_csv(out_path, header=True, index=True)
