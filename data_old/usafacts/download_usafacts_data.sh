#!/bin/bash
# this will change daily, check here: https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/ (updates around 9am)
# date is the date retrieved (includes cases up to but not including that day)

wget https://static.usafacts.org/public/data/covid-19/covid_confirmed_usafacts.csv?_ga=2.197512495.1424874733.1584823999-420321071.1584823999 -O confirmed_cases.csv
wget https://static.usafacts.org/public/data/covid-19/covid_deaths_usafacts.csv?_ga=2.197512495.1424874733.1584823999-420321071.1584823999 -O deaths.csv
