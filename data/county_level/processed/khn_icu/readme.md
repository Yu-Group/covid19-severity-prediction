# ICU Beds by County

- **Data source**: https://khn.org/news/as-coronavirus-spreads-widely-millions-of-older-americans-live-in-counties-with-no-icu-beds/

- **Last downloaded**: 04/06/2020

- **Data description**: provides number of hospitals and number of ICU beds per county, according to hospital cost reports filed to the Centers for Medicare & Medicaid Services; data provided by Kaiser Health News

- **Known data quality issues**: 
	- Some manual adjustments were made to correct errors in the hospital cost reports. Please see DOC/Readme_KHN.docx for details.

- **Short list of data columns**: 
	- **countyFIPS**: county FIPS
	- **#Hospitals**: number of hospitals in the Hospital Compare general information file, for each county
	- **#ICU_beds**: number of ICU beds reported in the most recent cost report for each hospital, including the categories "intensive care unit," "coronary care unit," "burn intensive care unit" and "surgical intensive care unit," aggregated by county
	- **60plusPerICUBed**: the population 60 and older divided by the total number of ICU_beds, where ICU_beds > 0

