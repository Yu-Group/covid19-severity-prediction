# NCHS Compressed Mortality File (2012-2016)

- **Data source**: https://wonder.cdc.gov/cmf-icd10.html

- **Last downloaded**: 04/02/2020

- **Data description**: includes mortality (deaths per 100,000) and population counts for all US counties; here, we pull data for the years 2012-2016, obtained from the National Center for Health Statistics Compressed Mortality File

- **Known data quality issues**: 
	- Due to confidentiality constraints, sub-national death counts and rates are suppressed (and listed as "NA") when the number of deaths is less than 10.
	- Other city-specific data quality issues are specified in the footnote of ```../raw/nchs_mortality.txt```

- **Short list of data columns**: 
	- **countyFIPS**: county FIPS
	- **CrudeMortalityRate2012-2016**: the number of deaths reported each calendar year per 100,000, reporting the death rate per 100,000 persons.

- **Notes**: 
	- See https://wonder.cdc.gov/wonder/help/cmf.html# for more information
	- Centers for Disease Control and Prevention, National Center for Health Statistics. Compressed Mortality File 1999-2016 on CDC WONDER Online Database, released June 2017. Data are from the Compressed Mortality File 1999-2016 Series 20 No. 2V, 2017