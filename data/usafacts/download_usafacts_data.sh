#!/bin/bash
# this will change daily, check here: https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/
# date is the date retrieved (includes cases up to but not including that day)

wget https://static.usafacts.org/public/data/covid-19/covid_confirmed_usafacts.csv?_ga=2.232244255.1424874733.1584823999-420321071.1584823999 -O confirmed_cases_mar22.csv
wget https://static.usafacts.org/public/data/covid-19/covid_deaths_usafacts.csv?_ga=2.234758174.1424874733.1584823999-420321071.1584823999 -O deaths_mar22.csv

# wget https://static.usafacts.org/public/data/covid-19/covid_confirmed_usafacts.csv?_ga=2.147834679.1204941409.1584826580-1312707976.1584826580 -O 01_usafacts_data.csv
