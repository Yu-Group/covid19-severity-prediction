#!/usr/bin/python3

import os

def download_nytimes_infections(data_dir="."):
    os.system("cd {}".format(data_dir))
    os.system("git clone https://github.com/nytimes/covid-19-data")
    os.system("cp ./covid-19-data/us-counties.csv .")
    os.system("rm -rf ./covid-19-data")
    os.system("mv us-counties.csv nytimes_infections.csv")

if __name__ == "__main__":
    download_nytimes_infections()
