# CMS Chronic Conditions Data (2017)

- **Data source**: https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Chronic-Conditions/CC_Main

- **Last downloaded**: 04/02/2020

- **Data description**: county-level prevalence of 21 chronic conditions based upon CMS administrative enrollment and claims data for Medicare beneficiaries enrolled in the fee-for-service program; data are available from the CMS Chronic Condition Data Warehouse

- **Known data quality issues**: 
	- Data are suppressed (and denoted by "\*") if there are fewer than 11 Medicare beneficiaries in the cell 

- **Short list of data columns**: 
	- **State**: state name
	- **County Name**: county name
	- **countyFIPS**: county FIPS
	- **MedicareCondition**: prevalence of the condition, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in our fee-for-service population (expressed as a percentage)

- **Notes**: 
	- A Medicare beneficiary is considered to have a chronic condition if the CMS administrative data have a claim indicating that the beneficiary received a service or treatment for the specific condition. Beneficiaries may have more than one of the chronic conditions listed.

