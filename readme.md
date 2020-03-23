Working to predict covid-19 risk at a county-level (in the US) and more.


# data setup
- get df_renamed.pkl from [here](https://drive.google.com/open?id=1OfeUn8RcOfkibgjtuuVt2z9ZtzC_4Eq5) and put into proper directory: data/hrsa/data_AHRF_2018-2019/processed/df_renamed.pkl 
- download usfacts data using script at data/usafacts/download_usafacts_data.sh
- download medicare data using script at data/medicare/download_medicare_data.sh
- get DiabetesAtlasCountyData.csv from [here](https://drive.google.com/open?id=1dfV8kEzVtMVzJKRyHVam9gsGq-WnvyHm) and put into proper directory: data/medicare/DiabetesAtlasCountyData.csv
- then, you should be able to load the data using the load_data.ipynb nb