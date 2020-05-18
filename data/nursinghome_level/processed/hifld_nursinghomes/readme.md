# HIFLD Nursing Homes Data (2020)

- **Data source**: https://hifld-geoplatform.opendata.arcgis.com/datasets/78c58035fb3942ba82af991bb4476f13_0

- **Last downloaded**: 05/12/2020

- **Data description**: database of nursing homes/assisted living facilities, populated via open source authoritative sources; data provided by the Homeland Infrastructure Foundation-Level Data platform

- **Known data quality issues**:
	- may have duplicates
	- some manual edits are documented and stored in hifld_nursinghomes_manualedits.csv
	- Note: to resolve duplicated nursing homes in MO, referenced https://health.mo.gov/information/boards/certificateofneed/pdf/rcfcty.pdf; for duplicated nursing homes in other states, differences were resolved manually

- **Short list of data columns**: 
	- **NAME**: name of nursing home facility
	- **ADDRESS**: address
	- **CITY**: city
	- **STATE**: state abbreviation
	- **ZIP**: ZIP code
	- **LATITUDE**: latitude
	- **LONGITUDE**: longitude
	- **County**: name of county
	- **countyFIPS**: county fips
	- **TYPE**: type of facility
	- **STATUS**: open or closed
	- **POPULATION**
	- **BEDS**
	- **TOT_RES**
	- **TOT_STAFF**
	- **EXCESS_BED**