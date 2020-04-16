#! /usr/bin/python3
import os
os.system("wget http://ghdx.healthdata.org/sites/default/files/record-attached-files/IHME_USA_COUNTY_RESP_DISEASE_MORTALITY_1980_2014_NATIONAL_XLSX.zip -O ihme_respiratory_raw.zip")
os.system("unzip ihme_respiratory_raw.zip")
os.system("mv IHME_USA_COUNTY_RESP_DISEASE_MORTALITY_1980_2014_NATIONAL_Y2017M09D26.XLSX ihme_respiratory.xlsx")
os.system("rm -f *.zip")