## List of columns - county level

- Variables in abridged data set (county_data_abridged.csv) are highlighted in bold.
- Most variables from Area Health Resources Files (AHRF) are not listed below. Only those AHRF variables in the abridged data set are included. Please see the AHRF user documentation for details on the other \~7000 variables (which includes data on county classifications, health professions, health facilities, utilization, expenditures, population, and environment)
- For full list of features in county_data.csv and their corresponding data set, see list_of_columns.csv


### Identifying variables
| Data variable     | Description |  Source data set |
| ---   | --- | --- |
|**countyFIPS**| state-county FIPS Code | county_fips |
|**STATEFP**| state FIPS Code | county_popcenters |
|**COUNTYFP**| county FIPS Code | county_popcenters |
|**CountyName**| county name | county_fips |
|**StateName**| state abbreviation | county_fips |
|**State**| state name | county_latlong |


### Data variables

#### Geographical identifiers
| Data variable     | Description | Source data set |
| ---   | --- | --- |
|**lat**| latitude corresponding to county's geographic center | county_latlong |
|**lon**| longitude corresponding to county's geographic center | county_latlong |
|**POP\_LATITUDE**| latitude corresponding to county's population center | county_popcenters |
|**POP\_LONGITUDE**| longitude corresponding to county's population center | county_popcenters |
|**CensusRegionName**| name of census region | ahrf_health |
|**CensusDivisionName**| name of census division | ahrf_health |
|**Rural-UrbanContinuumCode2013**| rural-urban continuum code | ahrf_health |
|HPSAName| name of the Health Professional Shortage Area (HPSA) name | hpsa_shortage |
|HPSAMetroIndicator| whether a Health Professional Shortage Area (HPSA) is either Metropolitan, Non-Metropolitan, or Frontier in nature | hpsa_shortage |
|HPSARuralStatus| rural, non-rural, or partially rural | hpsa_shortage|

#### Demographics
| Data variable     | Description | Source data set |
| ---   | --- | --- |
|HPSAPercentPoverty| percent of the population in the Health Professional Shortage Area (HPSA) living below the U.S. Federal Poverty Level | hpsa_shortage |
|**PopulationEstimate2018**| estimated total population of county in 2018 | ahrf_health |
|**PopulationEstimate65+2017**| estimated population of 65+ age group in county in 2017 | ahrf_health |
|**PopTotalMale2017**| total population of males in county in 2017 | ahrf_health |
|**PopTotalFemale2017**| total population of females in county in 2017 | ahrf_health |
|**PopulationDensityperSqMile2010**| population density per square mile in county in 2010| ahrf_health |
|**CensusPopulation2010**| 2010 census population of county | ahrf_health |
|**MedianAge2010**| median age of county in 2010 | ahrf_health|
|**MedianAge2010**| median age of county in 2010 | ahrf_health|
|**MedianAge2010**| median age of county in 2010 | ahrf_health|
|**#EligibleforMedicare2018**| number of people eligible for Medicare in county in 2018 | ahrf_health |
|**MedicareEnrollment,AgedTot2017**| medicare enrollment (based on age requirement) in the county in 2017 | ahrf_health |
|**PopMale<52010**| county population of males age < 5 from 2010 census | ahrf_health |
|**PopFmle<52010**| county population of females age < 5 from 2010 census | ahrf_health |
|**PopMale5-92010**| county population of males age 5-9 from 2010 census | ahrf_health |
|**PopFmle<5-92010**| county population of females age 5-9 from 2010 census | ahrf_health |
|**PopMale10-142010**| county population of males age 10-14 from 2010 census | ahrf_health |
|**PopFmle10-142010**| county population of females age 10-14 from 2010 census | ahrf_health |
|**PopMale15-192010**| county population of males age 15-19 from 2010 census | ahrf_health |
|**PopFmle15-192010**| county population of females age 15-19 from 2010 census | ahrf_health |
|**PopMale20-242010**| county population of males age 20-24 from 2010 census | ahrf_health |
|**PopFmle20-242010**| county population of females age 20-24 from 2010 census | ahrf_health |
|**PopMale25-292010**| county population of males age 25-29 from 2010 census | ahrf_health |
|**PopFmle25-292010**| county population of females age 25-29 from 2010 census | ahrf_health |
|**PopMale30-342010**| county population of males age 30-34 from 2010 census | ahrf_health |
|**PopFmle30-342010**| county population of females age 30-34 from 2010 census | ahrf_health |
|**PopMale35-442010**| county population of males age 35-44 from 2010 census | ahrf_health |
|**PopFmle35-442010**| county population of females age 35-44 from 2010 census | ahrf_health |
|**PopMale45-542010**| county population of males age 45-54 from 2010 census | ahrf_health |
|**PopFmle45-542010**| county population of females age 45-54 from 2010 census | ahrf_health |
|**PopMale55-592010**| county population of males age 55-59 from 2010 census | ahrf_health |
|**PopFmle55-592010**| county population of females age 55-59 from 2010 census | ahrf_health |
|**PopMale60-642010**| county population of males age 60-64 from 2010 census | ahrf_health |
|**PopFmle60-642010**| county population of females age 60-64 from 2010 census | ahrf_health |
|**PopMale65-742010**| county population of males age 65-74 from 2010 census | ahrf_health |
|**PopFmle65-742010**| county population of females age 65-74 from 2010 census | ahrf_health |
|**PopMale75-842010**| county population of males age 75-84 from 2010 census | ahrf_health |
|**PopFmle75-842010**| county population of females age 75-84 from 2010 census | ahrf_health |
|**PopMale>842010**| county population of males age > 84 from 2010 census | ahrf_health |
|**PopFmle>842010**| county population of females age > 84 from 2010 census | ahrf_health |
|% Uninsured| percentage of population under age 65 without health insurance (2017) | chrr_health |
|High School Graduation Rate| percentage of ninth-grade cohort that graduates in four years (2016-17) | chrr_health |
|% Some College| percentage of adults ages 25-44 with some post-secondary education (2014-18) | chrr_health |
|% Unemployed| percentage of population ages 16 and older unemployed but seeking work (2018) | chrr_health |
|% Children in Poverty| percentage of people under age 18 in poverty (2018) | chrr_health |
|Income Ratio| ratio of household income at the 80th percentile to income at the 20th percentile (2014-18) | chrr_health |
|% Single-Parent Households| percentage of children that live in a household headed by single parent (2014-18) | chrr_health |
|Social Association Rate| number of membership associations per 10,000 population (2017) | chrr_health |
|% Severe Housing Problems| percentage of households with at least 1 of 4 housing problems: overcrowding, high housing costs, lack of kitchen facilities, or lack of plumbing facilities (2012-16) | chrr_health |
|Urban Influence Code 2013| urban influence code 2013 | usda_poverty |
|Poverty Num All Ages 2018| estimate of people of all ages in poverty 2018 | usda_poverty |
|Poverty Num Ages 0-17 2018| estimate of people ages 0-17 in poverty 2018  | usda_poverty |
|Poverty Num Ages 5-17 2018| estimate of people ages 5-17 in poverty 2018 | usda_poverty |
|Poverty Pct All Ages 2018| estimate of percent of people of all ages in poverty 2018 | usda_poverty |
|Poverty Pct Ages 0-17 2018| estimate of percent of people ages 0-17 in poverty 2018  | usda_poverty |
|Poverty Pct Ages 5-17 2018| estimate of percent of people ages 5-17 in poverty 2018  | usda_poverty |
|Median Household Income 2018| median household income 2018 | usda_poverty |


#### Health Resource Availability

| Data variable     | Description | Source data set |
| ---   | --- | --- |
|**#Hospitals**| number of hospitals in the Hospital Compare general information file, for each county | khn_icu |
|**#ICU\_beds**| number of ICU beds reported in the most recent cost report for each hospital, including the categories "intensive care unit," "coronary care unit," "burn intensive care unit" and "surgical intensive care unit," aggregated by county | khn_icu |
|60plusPerICUBed| the population 60 and older divided by the total number of ICU_beds; NA if ICU_beds = 0 | khn_icu |
|**#FTEHospitalTotal2017**| number of full-time employees at hospitals in 2017 | ahrf_health |
|**TotalM.D.'s,TotNon-FedandFed2017**| number of MDs in each county in 2017 | ahrf_health |
|**#HospParticipatinginNetwork2017**| number of hospitals participating in network in 2017 | ahrf_health |
|**SVIPercentile**| the county's overall percentile ranking indicating the CDC's Social Vulnerability Index (SVI); higher ranking indicates greater social vulnerability | cdc_svi |
|SVIPercentileSEtheme| the county's percentile ranking from the SVI socioeconomic theme, which accounts for poverty level, unemployment, income, high school diploma; higher ranking indicates greater social vulnerability | cdc_svi |
|SVIPercentileHDtheme| the county's percentile ranking from the SVI housing composition and disability theme, which accounts for composition of those $\geq$ 65, $\leq$ 17, >5 with a disability, and single-parent households; higher ranking indicates greater social vulnerability | cdc_svi |
|SVIPercentileMLtheme| the county's percentile ranking from the SVI minority status and language theme, which accounts for minority status and if one speaks English "less than well"; higher ranking indicates greater social vulnerability | cdc_svi |
|SVIPercentileHTtheme| the county's percentile ranking from the SVI housing and transportation theme, which accounts for multi-unit structures, mobile homes, crowding, no vehicles, and group quarters; higher ranking indicates greater social vulnerability| cdc_svi |
|**HPSAScore**| the Health Professional Shortage Area Score developed by the NHSC in determining priorities for assignment of clinicians; ranges from 0 to 26 where the higher the score, the greater the priority | hpsa_shortage |
|HPSAServedPop| estimated total population served by the full-time equivalent (FTE) Health care practitioners within a (HPSA) | hpsa_shortage |
|HPSAUnderservedPop| estimated underserved population served by the full-time equivalent (FTE) health care practitioners within a HPSA | hpsa_shortage|
|**HPSAShortage**| the number of full-time equivalent (FTE) practitioners needed in the Health Professional Shortage Area (HPSA) so that it will achieve the population to practitioner target ratio; target ratio is determined by the type (discipline) of the HPSA | hpsa_shortage|
|Primary Care Physicians Ratio| ratio of population to primary care physicians (2017) | chrr_health |
|Dentist Ratio| ratio of population to dentists (2018) | chrr_health |
|Mental Health Provider Ratio| ratio of population to mental health providers (2019) | chrr_health |


#### Health Outcomes and Risk Factors

| Data variable     | Description | Source data set |
| ---   | --- | --- |
|**HeartDiseaseMortality**| estimated mortality rate per 100,000 (all ages, all races/ethnicities, both genders, 2014-2016) from all heart diseases | dhdsp_heart |
|**StrokeMortality**| estimated mortality rate per 100,000 (all ages, all races/ethnicities, both genders, 2014-2016) from all strokes | dhdsp_stroke |
|RespMortalityRate1980| estimated age-standardized mortality rates (deaths per 100,000) for both sexes combined for year 1980 | ihme_respiratory |
|RespMortalityRate1980LowCI95| lower limit of 95% confidence interval for mortality rate estimate for year 1980 | ihme_respiratory |
|RespMortalityRate1980HighCI95| upper limit of 95% confidence interval for mortality rate estimate for year 1980 | ihme_respiratory |
|RespMortalityRate1985| estimated age-standardized mortality rates (deaths per 100,000) for both sexes combined for year 1985 | ihme_respiratory |
|RespMortalityRate1985LowCI95| lower limit of 95% confidence interval for mortality rate estimate for year 1985 | ihme_respiratory |
|RespMortalityRate1985HighCI95| upper limit of 95% confidence interval for mortality rate estimate for year 1985 | ihme_respiratory |
|RespMortalityRate1990| estimated age-standardized mortality rates (deaths per 100,000) for both sexes combined for year 1990 | ihme_respiratory |
|RespMortalityRate1990LowCI95| lower limit of 95% confidence interval for mortality rate estimate for year 1990 | ihme_respiratory |
|RespMortalityRate1990HighCI95| upper limit of 95% confidence interval for mortality rate estimate for year 1990 | ihme_respiratory |
|RespMortalityRate1995| estimated age-standardized mortality rates (deaths per 100,000) for both sexes combined for year 1995 | ihme_respiratory |
|RespMortalityRate1995LowCI95| lower limit of 95% confidence interval for mortality rate estimate for year 1995 | ihme_respiratory |
|RespMortalityRate1995HighCI95| upper limit of 95% confidence interval for mortality rate estimate for year 1995 | ihme_respiratory |
|RespMortalityRate2000| estimated age-standardized mortality rates (deaths per 100,000) for both sexes combined for year 2000 | ihme_respiratory |
|RespMortalityRate2000LowCI95| lower limit of 95% confidence interval for mortality rate estimate for year 2000 | ihme_respiratory |
|RespMortalityRate2000HighCI95| upper limit of 95% confidence interval for mortality rate estimate for year 2000 | ihme_respiratory |
|RespMortalityRate2005| estimated age-standardized mortality rates (deaths per 100,000) for both sexes combined for year 2005 | ihme_respiratory |
|RespMortalityRate2005LowCI95| lower limit of 95% confidence interval for mortality rate estimate for year 2005 | ihme_respiratory |
|RespMortalityRate2005HighCI95| upper limit of 95% confidence interval for mortality rate estimate for year 2005 | ihme_respiratory |
|RespMortalityRate2010| estimated age-standardized mortality rates (deaths per 100,000) for both sexes combined for year 2010 | ihme_respiratory |
|RespMortalityRate2010LowCI95| lower limit of 95% confidence interval for mortality rate estimate for year 2010 | ihme_respiratory |
|RespMortalityRate2010HighCI95| upper limit of 95% confidence interval for mortality rate estimate for year 2010 | ihme_respiratory |
|**RespMortalityRate2014**| estimated age-standardized mortality rates (deaths per 100,000) for both sexes combined for year 2014 | ihme_respiratory |
|RespMortalityRate2014LowCI95| lower limit of 95% confidence interval for mortality rate estimate for year 2014 | ihme_respiratory |
|RespMortalityRate2014HighCI95| upper limit of 95% confidence interval for mortality rate estimate for year 2014 | ihme_respiratory |
|RespChangeInMortality1980-2014| estimated percent change in mortality rate between 1980 and 2014 | ihme_respiratory |
|RespChangeInMortality1980-2014LowCI95| lower limit of 95% confidence interval for percent change in mortality rate between 1980 and 2014 | ihme_respiratory |
|RespChangeInMortality1980-2014HighCI95| upper limit of 95% confidence interval for percent change in mortality rate between 1980 and 2014 | ihme_respiratory |
|MedicareAlcoholAbuse| prevalence of alcohol abuse, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareAlzheimers| prevalence of Alzheimers, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareArthritis| prevalence of Arthritis, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareAsthma| prevalence of Asthma, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareAtrialFibrillation| prevalence of atrial fibrillation, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareAutism| prevalence of Autism, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareCancer| prevalence of cancer, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareKidneyDisease| prevalence of kidney disease, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareCOPD| prevalence of COPD, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareDepression| prevalence of depression, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareDiabetes| prevalence of diabetes, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareDrugAbuse| prevalence of drug abuse, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareHIVAIDS| prevalence of HIV/AIDS, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareHertFailure| prevalence of heart failure, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareHepatitis| prevalence of hepatitis, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareHyperlipidemia| prevalence of Hyperlipidemia, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareHypertension| prevalence of hypertension, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareIschemic Heart Disease| prevalence of Ischemic Heart Disease, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareOsteoporosis| prevalence of Osteoporosis, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicarePsychotic Disorders| prevalence of psychotic disorders, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|MedicareStroke| prevalence of stroke, calculated by taking the beneficiaries with the given condition divided by the total number of beneficiaries in Medicare fee-for-service population (expressed as a percentage) | medicare_chronic |
|**DiabetesPercentage**| estimated age-adjusted percentage of diagnosed diabetes in 2016 among adults age 20 and over | usdss_diabetes |
|DiabetesLowCI95| lower limit of 95% confidence interval for diagnosed diabetes percentage | usdss_diabetes |
|DiabetesHighCI95| upper limit of 95% confidence interval for diagnosed diabetes percentage | usdss_diabetes |
|**3-YrDiabetes2015-17**| estimated percentage of diabetes | ahrf_health|
|CrudeMortalityRate2012-2016| the number of deaths reported each calendar year per 100,000, reporting the death rate per 100,000 persons | nchs_mortality |
|**3-YrMortalityAge<1Year2015-17**| mortality rate for population age < 1, averaged over 2015-17 | ahrf_health |
|**3-YrMortalityAge1-4Years2015-17**| mortality rate for population age 1-4, averaged over 2015-17 | ahrf_health |
|**3-YrMortalityAge5-14Years2015-17**| mortality rate for population age 5-14, averaged over 2015-17 | ahrf_health |
|**3-YrMortalityAge15-25Years2015-17**| mortality rate for population age 15-25, averaged over 2015-17 | ahrf_health |
|**3-YrMortalityAge25-34Years2015-17**| mortality rate for population age 25-34, averaged over 2015-17 | ahrf_health |
|**3-YrMortalityAge35-44Years2015-17**| mortality rate for population age 35-44, averaged over 2015-17 | ahrf_health |
|**3-YrMortalityAge45-54Years2015-17**| mortality rate for population age 45-54, averaged over 2015-17 | ahrf_health |
|**3-YrMortalityAge55-64Years2015-17**| mortality rate for population age 55-64, averaged over 2015-17 | ahrf_health |
|**3-YrMortalityAge65-74Years2015-17**| mortality rate for population age 65-74, averaged over 2015-17 | ahrf_health |
|**3-YrMortalityAge75-84Years2015-17**| mortality rate for population age 75-84, averaged over 2015-17 | ahrf_health |
|**3-YrMortalityAge85+Years2015-17**| mortality rate for population age 85+, averaged over 2015-17 | ahrf_health |
|Years of Potential Life Lost Rate| years of potential life lost before age 75 per 100,000 population (age-adjusted) (2016-2018) | chrr_health |
|% Fair or Poor Health| percentage of adults reporting fair or poor health (age-adjusted) (2017) | chrr_health |
|Average Number of Physically Unhealthy Days| average number of physically unhealthy days reported in past 30 days (age-adjusted) (2017) | chrr_health |
|Average Number of Mentally Unhealthy Days| average number of mentally unhealthy days reported in past 30 days (age-adjusted) (2017) | chrr_health |
|% Low Birthweight| percentage of live births with low birthweight (< 2,500 grams) (2012-18) | chrr_health |
|**Smokers\_Percentage**| estimated percentage of adult smokers in county (2017) | chrr_smoking |
|% Adults with Obesity| percentage of the adult population (age 20 and older) that reports a body mass index (BMI) greater than or equal to 30 kg/m2 (2016) | chrr_health |
|Food Environment Index| index of factors that contribute to a healthy food environment, from 0 (worst) to 10 (best) (2015, 2017) | chrr_health |
|% Physically Inactive| percentage of adults age 20 and over reporting no leisure-time physical activity (2016) | chrr_health |
|% With Access to Exercise Opportunities| percentage of population with adequate access to locations for physical activity (2010, 2019) | chrr_health |
|% Excessive Drinking**: percentage of adults reporting binge or heavy drinking (2017) | chrr_health |
|% Driving Deaths with Alcohol Involvement| percentage of driving deaths with alcohol involvement (2014-18) | chrr_health |
|Chlamydia Rate| number of newly diagnosed chlamydia cases per 100,000 population (2017) | chrr_health |
|Teen Birth Rate| number of births per 1,000 female population ages 15-19 (2012-18) | chrr_health |
|Preventable Hospitalization Rate| rate of hospital stays for ambulatory-care sensitive conditions per 100,000 Medicare enrollees  (2017) | chrr_health |
|% With Annual Mammogram| percentage of female Medicare enrollees ages 65-74 that received an annual mammography screening (2017) | chrr_health |
|% Vaccinated| percentage of fee-for-service (FFS) Medicare enrollees that had an annual flu vaccination (2017) | chrr_health |
|Violent Crime Rate| number of reported violent crime offenses per 100,000 population (2014, 2016) | chrr_health |
|Injury Death Rate| number of deaths due to injury per 100,000 population (2014-18) | chrr_health |
|Average Daily PM2.5| average daily density of fine particulate matter in micrograms per cubic meter (PM2.5) (2014) | chrr_health |
|Presence of Water Violation| indicator of the presence of health-related drinking water violations. 'Yes' indicates the presence of a violation, 'No' indicates no violation (2018) | chrr_health |
|observed_ili%Y-%m-%d| daily ILI incidence in the specified region on the specified date; from Kinsa thermometers | kinsa_ili |
|atypical_ili%Y-%m-%d| will contain the observed ILI from Kinsa if it is atypical; otherwise is null | kinsa_ili |
|anomaly_diff%Y-%m-%d| measure of how much atypical illness is present from Kinsa | kinsa_ili |
|forecast_expected%Y-%m-%d| where illness is expected to be based on time of year in given county from Kinsa | kinsa_ili |
|forecast_lower%Y-%m-%d| lower bound for expected forecast from Kinsa | kinsa_ili |
|forecast_upper%Y-%m-%d| upper bound for expected forecast | kinsa_ili |

		

#### Social Distancing and Mobility (private data)
| Data variable     | Description | Source data set |
| ---   | --- | --- |
|**daily\_distance\_diff%Y-%m-%d**| change of average distance traveled on %Y-%m-%d from baseline (avg. distance traveled for same day of week during pre-COVID-19 time period for a specific county); dating from 2/24/20 to present-day (minus few days lag) | unacast_mobility |
|daily\_visitation\_diff%Y-%m-%d| change of visits to non-essential retail and services on %Y-%m-%d from baseline (avg. visits for same day of week during pre-COVID-19 time period for a specific county); dating from 2/24/20 to present-day (minus few days lag) | unacast_mobility |
|encounter\_rate%Y-%m-%d| rate of unique human encounters per km^2 on %Y-%m-%d relative to national pre-COVID-19 baseline | unacast_mobility |
|VMT_per_capita%Y-%m-%d| total vehicle miles travelled by residents of county per capita on given date from Streetlight | streetlight_vmt |
|VMT_percent_change%Y-%m-%d| percent change in VMT on given date compared to VMT baseline from Streetlight | streetlight_vmt |
|device_count_{DATE}| number of devices seen in SafeGraph panel data on {DATE} whose home is in this countyFIPS | safegraph_socialdistancing |
|completely_home_device_county_{DATE}| out of the device_count, the number of devices which did not leave the geohash-7 in which their home is located on {DATE} | safegraph_socialdistancing |
|part_time_work_behavior_devices_{DATE}| out of the device_count, the number of devices that spent one period of between 3 and 6 hours at one location other than their geohash-7 home during the period of 8 am - 6 pm in local time | safegraph_socialdistancing |
|full_time_work_behavior_devices_{DATE}| out of the device_count, the number of devices that spent greater than 6 hours at a location other than their home geohash-7 during the period of 8 am - 6 pm in local time | safegraph_socialdistancing |
|delivery_behavior_devices_{DATE}| out of the device_count, the number of devices that stopped for < 20 minutes at > 3 locations outside of their geohash-7 home | safegraph_socialdistancing |
|bucketed\_distance\_traveled\_{BUCKET}\_{DATE}| {BUCKET} is range of meters (from geohash-7 of home) and value is the number of devices that fall into the given distance traveled bucket | safegraph_socialdistancing |
|bucketed_home_dwell_time\_{BUCKET}\_{DATE}| {BUCKET} is range of minutes and value is the number of devices that dwelled at geohash-7 of home for some time within the given {BUCKET} | safegraph_socialdistancing |
|bucketed_away_from_home_time\_{BUCKET}\_{DATE}| {BUCKET} is range of minutes and value is device count of devices that dwelled outside of geohash-7 of home for some time within the given {BUCKET} | safegraph_socialdistancing |
|bucketed_percentage_time_home\_{BUCKET}\_{DATE}| {BUCKET} is a range of percentage of time a device was observed at home (numerator) out of total hours observed that day at any location (denominator). Value is the number of devices observed in this {BUCKET} range. | safegraph_socialdistancing |
|at_home_by_each_hour\_{#}\_{DATE}| {#} is an hour of the day (e.g., 0 = midnight to 1am, 1 = 1am to 2am) and value is the number of devices at geohash-7 home in the given hour (in local time) | safegraph_socialdistancing |
|destination_cbgs\_{DATE}| dictionary; key is a destination countyFIPS and value is the number of devices with a home in the current (origin) countyFIPS that stopped in the given destination countyFIPS for >1 minute during the time period | safegraph_socialdistancing |
|n_places_{CATEGORY}| number of places (POIs) in countyFIPS for given industry category in SafeGraph panel data| safegraph_weeklypatterns |
|location_names_{CATEGORY}| list of locations in countyFIPS for given industry category in SafeGraph panel data | safegraph_weeklypatterns |
|naics_codes_{CATEGORY}| list of NAICS codes (i.e., industry categories) for each location in location_names_{CATEGORY} | safegraph_weeklypatterns |
|raw_visitor_counts_week\_{DATE}\_{CATEGORY}| list where the ith component corresponds to the number of unique visitors from panel to location i during the week starting on given {DATE} | safegraph_weeklypatterns |
|raw_visit_counts_week_{DATE}\_{CATEGORY}| list where the ith component corresponds to the number of visits in panel to location i during the week starting on given {DATE} | safegraph_weeklypatterns |
|visits_by_day_{DATE}\_{CATEGORY}| list where the ith component corresponds to the number of unique visitors from panel to location i on given date | safegraph_weeklypatterns |
|max_visits_in_hour_{DATE}\_{CATEGORY}| list where the ith component corresponds to the max number of visits to location i over the span of an hour on given date | safegraph_weeklypatterns |
|bucketed_dwell_times_{BUCKET}\_week\_{DATE}\_{CATEGORY}| list where the ith component corresponds to the number of visits to location i that were within the given time {BUCKET} duration over the span of the week starting on {DATE}; {BUCKET} is a range of minutes | safegraph_weeklypatterns |
|median_raw_visitor_counts_week_{DATE}\_{CATEGORY}| median of raw_visitor_counts_week\_{DATE}\_{CATEGORY} | safegraph_weeklypatterns |
|median_raw_visit_counts_week_{DATE}\_{CATEGORY}| median of raw_visit_counts_week_{DATE}\_{CATEGORY} | safegraph_weeklypatterns |
|sum_visits_by_day_{DATE}\_{CATEGORY}| sum of visits_by_day_{DATE}\_{CATEGORY} | safegraph_weeklypatterns |
|max_max_visits_in_hour_{DATE}\_{CATEGORY}| max of max_visits_in_hour_{DATE}\_{CATEGORY} | safegraph_weeklypatterns |
|sum_bucketed_dwell_times_{BUCKET}\_week\_{DATE}\_{CATEGORY}| sum of bucketed_dwell_times_{BUCKET}\_week\_{DATE}\_{CATEGORY} | safegraph_weeklypatterns |
|**stay at home**| contains the date that counties (or states governing them) took measures to mitigate the spread by restricting gatherings, given as the proleptic Gregorian ordinal of the date, where January 1 of year 1 has t = 1| jhu_interventions |
|**>50 gatherings**| contains the date that counties (or states governing them) took measures to mitigate the spread by restricting gatherings, given as the proleptic Gregorian ordinal of the date, where January 1 of year 1 has t = 1| jhu_interventions |
|**>500 gatherings**| contains the date that counties (or states governing them) took measures to mitigate the spread by restricting gatherings, given as the proleptic Gregorian ordinal of the date, where January 1 of year 1 has t = 1| jhu_interventions |
|**public schools**| contains the date that counties (or states governing them) took measures to mitigate the spread by restricting gatherings, given as the proleptic Gregorian ordinal of the date, where January 1 of year 1 has t = 1| jhu_interventions |
|**restaurant dine-in**| contains the date that counties (or states governing them) took measures to mitigate the spread by restricting gatherings, given as the proleptic Gregorian ordinal of the date, where January 1 of year 1 has t = 1| jhu_interventions |
|**entertainment/gym**| contains the date that counties (or states governing them) took measures to mitigate the spread by restricting gatherings, given as the proleptic Gregorian ordinal of the date, where January 1 of year 1 has t = 1| jhu_interventions |
|**federal guidelines**| contains the date that counties (or states governing them) took measures to mitigate the spread by restricting gatherings, given as the proleptic Gregorian ordinal of the date, where January 1 of year 1 has t = 1| jhu_interventions |
|**foreign travel ban**| contains the date that counties (or states governing them) took measures to mitigate the spread by restricting gatherings, given as the proleptic Gregorian ordinal of the date, where January 1 of year 1 has t = 1| jhu_interventions |
|% Drive Alone to Work| percentage of the workforce that drives alone to work (2014-18) | chrr_health |
|% Long Commute - Drives Alone| among workers who commute in their car alone, the percentage that commute more than 30 minutes (2014-18) | chrr_health |
|%Y-%m-%d_Parks| percent change in mobility at parks relative to baseline value for that day of the week | google_mobility |
|%Y-%m-%d_Residential| percent change in mobility at residential areas relative to baseline value for that day of the week | google_mobility |
|%Y-%m-%d_Retail-Recreation| percent change in mobility at retail and recreational areas relative to baseline value for that day of the week | google_mobility |
|%Y-%m-%d_Transit| percent change in mobility at transit areas relative to baseline value for that day of the week | google_mobility |
|%Y-%m-%d_Workplace| percent change in mobility at workplaces relative to baseline value for that day of the week | google_mobility |
|%Y-%m-%d_Grocery-Pharmacy| percent change in mobility at groceries and pharmacies relative to baseline value for that day of the week | google_mobility |


#### Miscellaneous
| Data variable     | Description | Source data set |
| ---   | --- | --- |
|**dem\_to\_rep\_ratio**| ratio of the number of votes received by the Democratic candidate over that received by the Republican candidate in the 2016 presidential election | mit_voting |



