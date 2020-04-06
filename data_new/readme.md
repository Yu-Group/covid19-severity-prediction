## Overview of all the data sets

The Yu group at UC Berkeley Statistics and EECS compiled and cleaned a large
corpus of hospital- and county-level data from a variety of public sources to
aid data science efforts to combat COVID-19. At the hospital level, our data
include the location of the hospital, the number of ICU beds, the total number
of employees, and the hospital type. At the county level, our data include
COVID-19 cases/deaths from USA Facts and NYT, automatically updated every day,
along with demographic information, health resource availability, COVID-19
health risk factors, and social mobility information. An overview of each data
set in this corpus is provided in this file.

We prepared this data to support emergency medical supply distribution efforts
through short-term (days) prediction of COVID-19 deaths (and cases) at the
county level. We are using the predictions and hospital data to arrive at a
covid Pandemic Severity Index (c-PSI) for each hospital. This project is in
partnership with [response4life.org](http://response4life.org). We will be
adding more relevant data sets as they are found.

An overview of each data set in this corpus is provided below:

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

    - **Health Risk Factors**
        - **chrr_smoking**: estimated percentage of adult smokers in each county from County Health Rankings & Roadmaps
        - **dhdsp_heart**: cardiovascular disease mortality rates from CDC DHDSP
        - **dhdsp_stroke**: stroke mortality rates from CDC DHDSP
        - **ihme_respiratory**: chronic respiratory disease mortality rates from IHME
        - **medicare_chronic**: Medicare claims data for 21 chronic conditions
        - **nchs_mortality**: overall mortality rates for each county from National Center for Health Statistics
        - **usdss_diabetes**: diagnosed diabetes in each county from CDC USDSS

    - **Social Distancing and Mobility/Miscellaneous**
        - **unacast_mobility**: county-level estimates of the change in mobility from pre-COVID-19 baseline from Unacast (private data)
        - **mit_voting**: county-level returns for presidential elections from 2000 to 2016 according to official state election data records


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
