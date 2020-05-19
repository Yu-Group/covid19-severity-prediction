# Google COVID-19 Community Mobility Reports

- **Data source**: https://www.google.com/covid19/mobility/

- **Last downloaded**: updated daily

- **Data description**: uses Google Maps data to report relative movement trends over time by geography and across different categories of places (e.g., retail and recreation, groceries and pharmacies, parks, transit stations, workplaces, and residential)

- **Known data quality issues**:
    - See About this data section at https://www.google.com/covid19/mobility/ for caveats and recommendations

- **Short list of data columns**:
	- **country_region_code**: country abbreviation
	- **country_region**: name of country
	- **sub_region1**: name of state (or province or any region bigger than county) (if applicable)
	- **sub_region2**: name of county (if applicable)
	- **date**: date
	- **retail_and_recreation_percent_change_from_baseline**: percent change in mobility at retail and recreation relative to baseline value for that day of the week
	- **grocery_and_pharmacy_percent_change_from_baseline**: percent change in mobility at groceries and pharamacies relative to baseline value for that day of the week
	- **parks_percent_change_from_baseline**: percent change in mobility  at parks relative to baseline value for that day of the week
	- **transit_stations_percent_change_from_baseline**: percent change in mobility at transit stations relative to baseline value for that day of the week
	- **workplaces_percent_change_from_baseline**: percent change in mobility at workplaces relative to baseline value for that day of the week
	- **residential_percent_change_from_baseline**: percent change in mobility at residential places relative to baseline value for that day of the week

- **Notes**:
    - Baseline value is the median value, for the corresponding day of the week, during the 5-week period Jan 3–Feb 6, 2020. 
    - For details, see data documentation: https://www.google.com/covid19/mobility/data_documentation.html?hl=en
    - Paper: Aktay, Ahmet, et al. "Google COVID-19 community mobility reports: Anonymization process description (version 1.0)." arXiv preprint arXiv:2004.04145 (2020).
    
    					