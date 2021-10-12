#!/usr/bin/python3

import os

def download_nytimes_infections(data_dir="."):
    os.system("cd {}".format(data_dir))
    os.system("wget https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv -O nytimes_infections.csv")

if __name__ == "__main__":
    download_nytimes_infections()
