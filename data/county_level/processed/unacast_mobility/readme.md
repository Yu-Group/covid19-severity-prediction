# Unacast Social Mobility and Distancing

- **Data source**: https://www.unacast.com/covid19/social-distancing-scoreboard

- **Last downloaded**: updated daily (exact date/time provided in data)

- **Data description**: county-level estimates of the change in mobility from pre-COVID-19 baseline. The change in mobility is quanified by 1) change in number of visits to non-essential retail and services from baseline and 2) change in average distance traveled from baseline.

- **Known data quality issues**: 
    - There is a 3-4 day lag in the data.
    - Daily visitation difference data is missing for 981 counties.

- **Short list of data columns**: 
    - **countyFIPS**: county FIPS
    - **daily_distance_diff%Y-%m-%d**: change of average distance traveled on %Y-%m-%d from baseline (avg. distance traveled for same day of week during pre-COVID-19 time period for a specific county)
    - **daily_visitation_diff%Y-%m-%d**: change of visits to non-essential retail and services on %Y-%m-%d from baseline (avg. visits for same day of week during pre-COVID-19 time period for a specific county)
    - **encounter_rate%Y-%m-%d**: rate of unique human encounters per km^2 on %Y-%m-%d relative to national pre-COVID-19 baseline (median of the metric on a country level in 4 weeks before March 8)

- **Notes**:

	- Current methodology:
        - "Essential” comprises grocery, pharmacy, and pet supplies; and “non-essential” comprises all other non-grocery retail goods and services. 
        - The pre-COVID-19 baseline is the 4 weeks prior to 03-08-2020. Data from the present-day is compared to the average of that day of the week for those 4 weeks.
        - A person is assigned to the county in which the device spends most of the day.
        - There are 15-17 million identifiers per day in the data set.
    - Thank you to Unacast for kindly sharing their data with us.