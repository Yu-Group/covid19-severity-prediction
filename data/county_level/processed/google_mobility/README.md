# Google COVID-19 Community Mobility Reports

- **Data source**: https://www.google.com/covid19/mobility/

- **Last downloaded**: updated daily

- **Data description**: uses Google Maps data to report relative movement trends over time by geography and across different categories of places (e.g., retail and recreation, groceries and pharmacies, parks, transit stations, workplaces, and residential)

- **Known data quality issues**:
    - See About this data section at https://www.google.com/covid19/mobility/ for caveats and recommendations

- **Short list of data columns**: (data in long format)
    - **Region Type**: level of granularity; one of {County, State, Country}
    - **Country**: name of country
    - **State/Province**: name of state (or province or any region bigger than county) (if applicable)
    - **County**: name of county (if applicable)    
    - **Date**: date
    - **Sector**: one of {parks, retail_and_recreation, transit, workplaces, residential, grocery_and_pharmacy}
    - **Percent Change**: percent change in mobility relative to baseline value for that day of the week

- **Notes**:
    - Baseline value is the median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020. 
    - For details, see data documentation: https://www.google.com/covid19/mobility/data_documentation.html?hl=en
    - Paper: Aktay, Ahmet, et al. "Google COVID-19 community mobility reports: Anonymization process description (version 1.0)." arXiv preprint arXiv:2004.04145 (2020).
    