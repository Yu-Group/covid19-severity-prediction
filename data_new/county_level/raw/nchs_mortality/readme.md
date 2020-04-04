# NCHS Compressed Mortality File (2012-2016)

- **Data source**: https://wonder.cdc.gov/cmf-icd10.html

- **Last downloaded**: 04/02/2020

- **Data description**: includes mortality (deaths per 100,000) and population counts for all US counties; here, we pull data for the years 2012-2016, obtained from the National Center for Health Statistics Compressed Mortality File

- **Known data quality issues**: 
	- Due to confidentiality constraints, sub-national death counts and rates are suppressed when the number of deaths is less than 10.
	- Death rates are flagged as Unreliable when the rate is calculated with a numerator of 20 or less.
	- Other city-specific data quality issues are specified in the footnote of ```nchs_mortality.txt```

- **Short list of data columns**: 
	- **County**: county name
	- **County Code**: county FIPS
	- **Deaths**: number of deaths in the legal place of residence of the decedent, summed over 2012-2016; data representing fewer than ten persons (0-9) are suppressed
	- **Population**: population of county, summed over 2012-2016
	- **Crude Rate**: the number of deaths reported each calendar year per 100,000, reporting the death rate per 100,000 persons.

- **Notes**: 
	- See https://wonder.cdc.gov/wonder/help/cmf.html# for more information
	- Centers for Disease Control and Prevention, National Center for Health Statistics. Compressed Mortality File 1999-2016 on CDC WONDER Online Database, released June 2017. Data are from the Compressed Mortality File 1999-2016 Series 20 No. 2V, 2017