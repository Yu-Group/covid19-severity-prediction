Working to predict covid-19 ventilator-demand (in the US) and more.


# quickstart
1. download the processed data (as a pickled dataframe `df_county_level_cached.pkl`) from [this folder](https://drive.google.com/drive/u/2/folders/1OfeUn8RcOfkibgjtuuVt2z9ZtzC_4Eq5) and place into the `data` directory
2. Can now load/merge the data:
```python
import load_data
df = load_data.load_county_level(data_dir='/path/to/data')
print(df.shape) # (1212, 7306)
```
- note: (non-cumulative) daily cases + deaths are in `data/usafacts/confirmed_cases.csv` and `data/usafacts/deaths.csv` (updated daily)
- note: abridged csv with county-level info such as demographics, hospital information, risk factors, and voting data is at `data/df_county_level_abridged_cached.csv`

- for an intro to some of the analysis here, visit the project webpage: https://yu-group.github.io/covid-19-ventilator-demand-prediction/outline


## related county-level projects
- https://github.com/JieYingWu/COVID-19_US_County-level_Summaries
- https://github.com/COVIDmodeling/covid_19_modeling

# forecasting county-level covid-19 deaths
- To get deaths predictions of the naive exponential growth model, the simplest way is to call
```python
df = exponential_modeling.estimate_deaths(df, target_day=np.array([...]))

# df is county level dataFrame
# target_day: time horizon, target_day=np.array([1]) predicts the next day, target_day=np.array([1, 2, 3]) predicts next 3 days, etc.
# return: dataFrame with new column 'predicted_deaths_exponential' 
```

The model training and visualization pipeline lives in:
modeling/basic_model_framework.ipynb
which will train and visualize the outputs of various models.

The high level wrapper for training and predicting values is the fit_and_predict function in 
modeling/fit_and_predict.py
this allows you to train a few models by passing in different arguments. For more details please see the function documentation.


    
# ventilator demand prediction


1. **Goal:** prioritizing where ventilators go
2. **Approach** 
    - predict ventilator demand + supply at the county-level 
    - filter hospitals and rank them according to their demand for additional ventilators
3. **Data** 
    - county-level: daily confirmed cases + deaths, demographics, comorbidity statistics, voting data, local gov. action data
    - hospital-level: information about hospitals (e.g. number of icu beds, hospital type, location)    
4. **Limitations**
    - currently using proxies for ventilator supply and demand instead of real measurements
    - limited data on bridging county-level data with hospital-level data


# 1 - goal: prioritizing where ventilators go

- working with [response4life](https://response4life.org/)
- would like to prioritize where to send available ventilators
- ideally, this would be where the ventilators could do the most "good" (e.g. save the most lives, minimize the Years of Life lost)

# 2 - approach

- begin by screening for large (academic) hospitals, which can accomodate more ventilators
- **outcomes**: we predict 2 things
    1. ventilator need - as a proxy for ventilator need, we predict the number of deaths (per county)
        - we estimate the ventilator need by scaling up the total number of expected deaths
        - here, we use many features at the county-level, such as demographics, comorbidity statistics, voting data
        - we are also trying to build in something local gov. action data (e.g. what has been enacted by local governments)
        - would like to use information directly from the hospital as well
        - this might also take into account some of the ventilator preparedness
    2. ventilator supply - as a proxy for current ventilator counts, we use the number of icu beds (per hospital)
        - hopefully, we can get some of this data from hospitals directly (although it might be sensitive)
        - in reality, there are more ventilators than icu beds
        - some ventilators (maybe 10-20%) will still be needed for non-covid-19 use
        - we would also like to build in something local gov. action data (e.g. what has been enacted by local governments)
        - would like to use information directly from the hospital as well
        - some hospitals are taking measures now to increase their number of ICU beds
        - government also has some stockpiled ventilators, although still unclear where they are
- using these outcomes, we then would like to prioritize different hospitals using a metric like: *ventilator need* (2-3 * # deaths) - *ventilator supply*
- these efforts should be coordinated with how the gov. is distributing ventilator stockpiles
- prediction setup
    - we restrict our analysis to counties which already have confirmed cases
    - each day, we randomly split counties to do prediction


# 3 - data

we have some data at the county-level and some at the hospital-level, which we jointly use to evaluate hospital need

## county-level data

- daily number of confirmed cases + deaths (from usafacts)
- population density, age distribution, gender distribution, presidential voting data, risk factors from medicare (e.g. diabetes, respiratory disease, ...), hospital data (e.g. # of doctors, # of hospitals, # of icu beds), and more demographic/disease data

## outbreak at the county-level
We can plot the outbreak for the counties with the highest number of deaths so far (updated daily):
<figure class="video_container" style="text-align: center">
  <iframe src="https://yu-group.github.io/covid-19-ventilator-demand-prediction/results/county_curves.html" frameborder="0" allowfullscreen="true" style="width:140%;height:1600px;"> </iframe>
</figure>

# full data sources

Only need to download these if you want to rerun the scraping / preprocessing pipeline.

## from google drive
- **[hrsa data](https://data.hrsa.gov/data/download)**: get df_renamed.pkl from [here](https://drive.google.com/open?id=1OfeUn8RcOfkibgjtuuVt2z9ZtzC_4Eq5) and put into proper directory: `data/hrsa/data_AHRF_2018-2019/processed/df_renamed.pkl`
    - provides demographics, income estimates, some mortality rates, hospital numbers, and more (all per county)
- **[voting data](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/VOQCHQ)**: download `county_voting_processed.pkl` from [here](https://drive.google.com/drive/u/2/folders/1OfeUn8RcOfkibgjtuuVt2z9ZtzC_4Eq5) and put into proper directory `data/voting/county_voting_processed.pkl`
    - ratio of votes in each county of democrat : republican in 2016 election
- **[diabetes data](https://gis.cdc.gov/grasp/diabetes/DiabetesAtlas.html#)**: DiabetesAtlasCountyData.csv from [here](https://drive.google.com/open?id=1dfV8kEzVtMVzJKRyHVam9gsGq-WnvyHm) and put into proper directory: data/diabetes/DiabetesAtlasCountyData.csv
    - diabetes rate per county
- **[respiratory disease data](http://ghdx.healthdata.org/record/ihme-data/united-states-chronic-respiratory-disease-mortality-rates-county-1980-2014)**: `IHME_USA_COUNTY_RESP_DISEASE_MORTALITY_1980_2014_NATIONAL_Y2017M09D26.XLSX` from [here](https://drive.google.com/drive/u/2/folders/1OfeUn8RcOfkibgjtuuVt2z9ZtzC_4Eq5) and place at `data/respiratory_disease/`
    - respiratory disease mortality rate per county
- **[icu beds data](https://khn.org/news/as-coronavirus-spreads-widely-millions-of-older-americans-live-in-counties-with-no-icu-beds/)**: download `icu_county.csv` from [here](https://drive.google.com/drive/u/2/folders/1OfeUn8RcOfkibgjtuuVt2z9ZtzC_4Eq5) and put into proper directory `data/icu/icu_county.pkl`
    - number of icu beds per county
- **[heart disease data](https://nccd.cdc.gov/DHDSPAtlas/?state=County)**: heart_disease_mortality_data.csv from [here](https://drive.google.com/open?id=1glMZ7l6UxYTjBUvvFNV7Hu8QXC-j5q3C) and put into proper directory: `data/cardiovascular_disease/heart_disease_mortality_data.csv`
- **[stroke data](https://nccd.cdc.gov/DHDSPAtlas/?state=County)**: stroke_mortality_data.csv from [here](https://drive.google.com/open?id=1ozVEjSGaQcRfJYnicKvEimKpAD3umI7o) and put into proper directory: `data/cardiovascular_disease/stroke_mortality_data.csv`
- **[mortality data](https://wonder.cdc.gov/cmf-icd10.html)**: Compressed Mortality, 2012-2016.txt from [here](https://drive.google.com/open?id=1xdscgVTtM30WuR3YUYVTdgC4IbTwdFZ_) and put into proper directory: `data/mortality/Compressed Mortality, 2012-2016.txt`; mortality rates (per year and per county) are also available by age group
- **countyFIPS**: in `data_hospital_level/processed/02_county_FIPS.csv.`
    - county identifier


## through scripts
- **confirmed cases + deaths - [usafacts data](https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/) (updated daily)**: using script at `data/usafacts/download_usafacts_data.sh`
- **[medicare data](https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Chronic-Conditions)**: using script at `data/medicare/download_medicare_data.sh`
- **[tobacco-use data](https://www.countyhealthrankings.org/explore-health-rankings/measures-data-sources/county-health-rankings-model/health-factors/health-behaviors/tobacco-use/adult-smoking)**: using script at `data/tobacco/download_tobacco_use_data.sh`i

## hospital-level data
- [list of academic hospitals](https://www.cms.gov/OpenPayments/Downloads/2020-Reporting-Cycle-Teaching-Hospital-List-PDF-.pdf)
- **private hospital-level data**: available in slack channel, rename to `04_hospital_level_info_merged_website.csv` put into `data_hospital_level/processed/04_hospital_level_info_merged_website.csv`
    - also can download some of the datasets using the scripts in the data_hospital_level directory

# 4 - results

## interactive visualizations

We can visualize these features on interactive maps:
<figure class="video_container">
  <iframe src="https://yu-group.github.io/covid-19-ventilator-demand-prediction/results/NY.html" frameborder="0" allowfullscreen="true" style="width:150%;height:1600px;"> </iframe>
</figure>

## correlations between county-level features and number of deaths
Correlations with number of deaths

![](results/correlations.png)

## all correlations

Correlations between many different county-level features
![](results/correlations_heatmap.png)



## hospital-level data

- key predictors: icu beds, total staff, location info, ratings, hospital type
- some of this data is not public so we can't share it all here
- potentially contact information and more we are still merging in...


## hospital-level employee time

- ICU Beds/Nurses ~ 4-8%
- Nurses / Total Employees ~ 20-40%
- Total Employees in top 4 states (NY/TX/CA/OH) ~ 1M.


# acknowledgements

The UC Berkeley Departments of Statistics, EECS and IEOR led by Professor Bin Yu

- Yu Group team (alphabetical order): Nick Altieri, Raaz Dwivedi, Xiao Li, Robbie Netzorg, Chandan Singh, Yan Shuo Tan, Tiffany Tang, Yu Wang
- Shen Group tean (alphabetical order): Junyu Cao, Shunan Jiang, Pelagie Elimbi Moudio
- the response4Life team and volunteers
- Helpful input from many including (alphabetical order): SriSatish Ambati, Rob Crockett, Marty Elisco, Samuel Scarpino, Suzanne Tamang, Tarek Zohdi
