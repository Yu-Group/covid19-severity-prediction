# COVID-19 Reported Patient Impact and Hospital Capacity by Facility

- **Data source**: https://healthdata.gov/dataset/covid-19-reported-patient-impact-and-hospital-capacity-facility

- **Last downloaded**: pulled directly from source which is updated weekly

- **Data description**: This data, provided by the US Department of Health and Human Services, provides facility-level data for hospital utilization aggregated on a weekly basis (Friday to Thursday). These are derived from reports with facility-level granularity across two main sources: (1) HHS TeleTracking, and (2) reporting provided directly to HHS Protect by state/territorial health departments on behalf of their healthcare facilities. Data is available starting on July 31, 2020.

- **Known data quality issues**: 
	- NAs denoted as -999999

- **Short list of data columns**: 
	- **collection_week**: start of the (weekly) period for which the data is collected and aggregated
	- **ccn**: CMS Certification Number (hospital ID)
	- **hospital_name**: name of hospital
	- **address**: address of hospital
	- **city**: city of hospital
	- **zip**: zip code of hospital
	- **state**: state of hospital
	- **fips_code**: county FIPS
	- A "\_coverage" append denotes how many times the facility reported that element during that collection week.
	- A "\_sum" append denotes the sum of the reports provided for that facility for that element during that collection week.
	- A "\_avg" append is the average of the reports provided for that facility for that element during that collection week.
	- Columns include data on total beds, total icu beds, total patients hospitalized with the flu or covid, and more

- **Notes**:
	- Further documentation can be found [here](https://healthdata.gov/dataset/covid-19-reported-patient-impact-and-hospital-capacity-facility)
	- Note that the hospital population includes all hospitals registered with Centers for Medicare & Medicaid Services (CMS) as of June 1, 2020. It includes non-CMS hospitals that have reported since July 15, 2020. It does not include psychiatric, rehabilitation, Indian Health Service (IHS) facilities, U.S. Department of Veterans Affairs (VA) facilities, Defense Health Agency (DHA) facilities, and religious non-medical facilities.



    