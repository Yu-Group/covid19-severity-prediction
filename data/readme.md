## Overview of all the data sets

**Overview below, detailed documentation in the [list of columns](list_of_columns.md)

The Yu group at UC Berkeley Statistics and EECS has compiled, cleaned and documented
a large corpus of hospital- and county-level data from a variety of public sources to
aid data science efforts to combat COVID-19. At the hospital level, our data
include the location of the hospital, the number of ICU beds, the total number
of employees, and the hospital type. At the county level, our data include
COVID-19 cases/deaths from USA Facts and NYT, automatically updated every day,
along with demographic information, health resource availability, COVID-19
health risk factors, and social mobility information. An overview of each data
set in this corpus is provided in this file.

An overview of each data set in this corpus is provided below. The data is also available on the AWS Data Exchange [here](https://aws.amazon.com/marketplace/pp/prodview-px2tvvydirx4o?qid=1587582026402&sr=0-1&ref_=srh_res_product_title#overview).

- **Hospital Level Data**
    - **cms_cmi**: Case Mix Index for hospitals from CMS 
    - **cms_hospitalpayment**: Teaching Hospital info from CMS
    - **DH_hospital**: US Hospital info from Definitive Healthcare
    - **hifld_hospital**: Hospital info from homeland infrastructue foundation level data

- **County Level Data**
    - **COVID-19 Cases/Deaths Data**
        - **nytimes_infections**: COVID-19-related death/case counts per day per county from NYT
        - **usafacts_infections**: COVID-19-related death/case counts per day per county from USA Facts

    - **Demographics and Health Resource Availability**
        - **ahrf_health**: contains county-level information on health facilities, health professions, measures of resource scarcity, health status, economic activity, health training programs, and socioeconomic and environmental characteristics from Area Health Resources Files
        - **cdc_svi**: Social Vulnerability Index for counties from CDC
        - **hpsa_shortage**: information on areas with shortages of primary care, as designated by the Health Resources & Services Administration (HRSA)
        - **khn_icu**: information on number of ICU beds and hospitals per county from Kaiser Health News
        - **usda_poverty**: county-level poverty estimates from the United States Department of Agriculture, Economic Research Service

    - **Health Risk Factors**
        - **chrr_health**: contains estimates of various health outcomes and health behaviors (e.g., percentage of adult smokers) for each county from County Health Rankings & Roadmaps
        - **dhdsp_heart**: cardiovascular disease mortality rates from CDC DHDSP
        - **dhdsp_stroke**: stroke mortality rates from CDC DHDSP
        - **ihme_respiratory**: chronic respiratory disease mortality rates from IHME
        - **medicare_chronic**: Medicare claims data for 21 chronic conditions
        - **nchs_mortality**: overall mortality rates for each county from National Center for Health Statistics
        - **usdss_diabetes**: diagnosed diabetes in each county from CDC USDSS
        - **kinsa_ili**: measures of anomalous influenza-like illness incidence (ILI) outbreaks in real-time using Kinsa’s county-level illness signals, developed from real-time geospatial thermometer data (private data)

    - **Social Distancing and Mobility/Miscellaneous**
        - **unacast_mobility**: county-level estimates of the change in mobility from pre-COVID-19 baseline from Unacast (private data)
        - **streetlight_vmt**: estimates of total vehicle miles travelled (VMT) by residents of each county, each day; provided by Streetlight Data (private data)
        - **safegraph_socialdistancing**: aggregated daily views of USA foot-traffic summarizing movement between counties from SafeGraph (private data)
        - **safegraph_weeklypatterns**: place foot-traffic and demographic aggregations that answer: how often people visit, where they came from, where else they go, and more; from SafeGraph (private data)
        - **jhu_interventions**: contains the dates that counties (or states governing them) took measures to mitigate the spread by restricting gatherings (e.g., travel bans, stay at home orders)
        - **mit_voting**: county-level returns for presidential elections from 2000 to 2016 according to official state election data records

- **Miscellaneous Data**
	- **bts_airtravel**: survey data including origin, destination, and itinerary details from a 10% sample of airline tickets from the Bureau of Transportation Statistics


## Quickstart
To load the county-level data (daily COVID-19 cases/deaths data + other county-level features listed above) from the project root directory:
```python
import data
# unabridged
df_unabridged = data.load_county_data(data_dir = "data", cached = False, abridged = False)
# abridged
df_abrdiged = data.load_county_data(data_dir = "data", cached = False, abridged = True)
```


## Folder Structure 
In this folder, we collect the useful hospital level data from a variety of sources. The structure of the folder is as the following:
- raw (contains raw data)
    - [datasource]_[shortname]/
        - load.py (a script that loads the data)
        - download.py (a script that downloads the data)
        - raw data
        - Readme.md (metadata for the raw data)
- processed (contains the processed data)
    - [datasource]_[shortname]/
        - clean.py (a script that cleans the data)
        - cleaned data
        - Readme.md (metadata for the cleaned data)


We prepared this data to support emergency medical supply distribution efforts
through short-term (days) prediction of COVID-19 deaths (and cases) at the
county level. We are using the predictions and hospital data to arrive at a
covid Pandemic Severity Index (c-PSI) for each hospital. This project is in
partnership with [response4life.org](http://response4life.org). We will be
adding more relevant data sets as they are found.