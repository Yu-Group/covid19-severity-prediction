Working to predict covid-19 risk at a county-level (in the US) and more.


# quickstart
- download `df_county_level_cached.pkl` from [this folder](https://drive.google.com/drive/u/2/folders/1OfeUn8RcOfkibgjtuuVt2z9ZtzC_4Eq5) and place into the `data` directory
- ready to run all notebooks on the county level!


# full data sources

Only need to download these if you want to rerun the scraping / preprocessing pipeline

## from google drive
- **[hrsa data](https://data.hrsa.gov/data/download)**: get df_renamed.pkl from [here](https://drive.google.com/open?id=1OfeUn8RcOfkibgjtuuVt2z9ZtzC_4Eq5) and put into proper directory: `data/hrsa/data_AHRF_2018-2019/processed/df_renamed.pkl`
    - provides 
- **voting data**: download `county_voting_processed.pkl` from [here](https://drive.google.com/drive/u/2/folders/1OfeUn8RcOfkibgjtuuVt2z9ZtzC_4Eq5) and put into proper directory `data/voting/county_voting_processed.pkl`
- **diabetes data**: DiabetesAtlasCountyData.csv from [here](https://drive.google.com/open?id=1dfV8kEzVtMVzJKRyHVam9gsGq-WnvyHm) and put into proper directory: data/diabetes/DiabetesAtlasCountyData.csv
- **respiratory disease data**: `IHME_USA_COUNTY_RESP_DISEASE_MORTALITY_1980_2014_NATIONAL_Y2017M09D26.XLSX` from [here](https://drive.google.com/drive/u/2/folders/1OfeUn8RcOfkibgjtuuVt2z9ZtzC_4Eq5) and place at `data/respiratory_disease/``
- **icu beds data**: download `icu_county.csv` from [here](https://drive.google.com/drive/u/2/folders/1OfeUn8RcOfkibgjtuuVt2z9ZtzC_4Eq5) and put into proper directory `data/icu/icu_county.pkl`
- **heart disease data**: heart_disease_mortality_data.csv from [here](https://drive.google.com/open?id=1glMZ7l6UxYTjBUvvFNV7Hu8QXC-j5q3C) and put into proper directory: `data/cardiovascular_disease/heart_disease_mortality_data.csv`
- **stroke data**: stroke_mortality_data.csv from [here](https://drive.google.com/open?id=1ozVEjSGaQcRfJYnicKvEimKpAD3umI7o) and put into proper directory: `data/cardiovascular_disease/stroke_mortality_data.csv`
- **countyFIPS**: in `data_hospital_level/processed/02_county_FIPS.csv.`

## through scripts
- **confirmed cases + deaths - [usafacts data](https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/) (updated daily)**: using script at `data/usafacts/download_usafacts_data.sh`
- **[medicare data](https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Chronic-Conditions)**: using script at `data/medicare/download_medicare_data.sh`
- **[tobacco-use data](https://www.countyhealthrankings.org/)**: using script at `data/tobacco/download_tobacco_use_data.sh`i

## private
- **hospital-level data**: available in slack channel, rename to `hospital_level_info_merged.csv` put into `data_hospital_level/processed/hospital_level_info_merged.csv`
    - also can download some of the datasets using the scripts in the data_hospital_level directory

if all is downloaded properly, you should be able to load the data using `load_data.py`