Working to predict covid-19 risk at a county-level (in the US) and more.


# data setup
## from google drive
- **hrsa data**: get df_renamed.pkl from [here](https://drive.google.com/open?id=1OfeUn8RcOfkibgjtuuVt2z9ZtzC_4Eq5) and put into proper directory: data/hrsa/data_AHRF_2018-2019/processed/df_renamed.pkl 
- **voting data**: download `county_voting_processed.pkl` from [here](https://drive.google.com/drive/u/2/folders/1OfeUn8RcOfkibgjtuuVt2z9ZtzC_4Eq5) and put into proper directory data/voting/county_voting_processed.pkl
- **diabetes data**: DiabetesAtlasCountyData.csv from [here](https://drive.google.com/open?id=1dfV8kEzVtMVzJKRyHVam9gsGq-WnvyHm) and put into proper directory: data/medicare/DiabetesAtlasCountyData.csv

## through scripts
- **usafacts data**: using script at data/usafacts/download_usafacts_data.sh
- **medicare data**: using script at data/medicare/download_medicare_data.sh


if all is downloaded properly, you should be able to load the data using `00_load_data_county_level.ipynb`