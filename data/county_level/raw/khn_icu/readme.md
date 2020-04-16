# ICU Beds by County

- **Data source**: https://khn.org/news/as-coronavirus-spreads-widely-millions-of-older-americans-live-in-counties-with-no-icu-beds/

- **Last downloaded**: 04/06/2020

- **Data description**: provides number of hospitals and number of ICU beds per county, according to hospital cost reports filed to the Centers for Medicare & Medicaid Services; data provided by Kaiser Health News

- **Known data quality issues**: 
	- Some manual adjustments were made to correct errors in the hospital cost reports. Please see DOC/Readme_KHN.docx for details.

- **Short list of data columns**: 
	- **cnty_fips**: county FIPS
	- **hospitals_in_cost_reports**: number of hospitals that filed a cost report since the beginning of 2018, for each county
	- **Hospitals_in_HC**: number of hospitals in the Hospital Compare general information file, for each county
	- **all_icu**: number of ICU beds reported in the most recent cost report for each hospital, including the categories "intensive care unit," "coronary care unit," "burn intensive care unit" and "surgical intensive care unit," aggregated by county
	- **Total_pop**: the total population for each county according to the 2017 five-year ACS
	- **60plus**: total population for each county that is 60 or older
	- **60plus_pct**: the percent of the total population that is 60 or older
	- **60plus_per_each_icu_bed**: the population 60 and older divided by the total number of ICU_beds, where ICU_beds > 0


- **Notes**:
	- Further details can be found in DOC/Readme_KHN.docx
	- Terms of Use provided in DOC/