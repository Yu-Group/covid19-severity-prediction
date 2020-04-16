# Streelight Data Vehicle Miles Traveled

- **Data source**: https://www.streetlightdata.com/VMT-monitor-by-county/

- **Last downloaded**: updated 2-3 times a week

- **Data description**: provides estimates of total vehicle miles travelled (VMT) by residents of each county, each day since the COVID-19 crisis began, as well as a change from the “baseline” (defined as the average daily VMT of January 2020); data provided by Streetlight Data

- **Known data quality issues**: 
    - There is a 2 day lag in the data.

- **Short list of data columns**: 
    - **countyFIPS**: county FIPS
    - **VMT_per_capita%Y-%m-%d**: total vehicle miles travelled by residents of county per capita on given date
    - **VMT_percent_change%Y-%m-%d**: percent change in VMT on given date compared to VMT baseline (i.e., January average VMT)

- **Notes**:
    - For more on methodology, please see https://learn.streetlightdata.com/vmt-monitor-methodology
    - Thank you to Streetlight Data for kindly sharing their data with us.