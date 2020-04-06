## List of columns - county level

- Variables in abridged data set (county_data_abridged.csv) are highlighted in bold.
- Most variables from Area Health Resources Files (AHRF) are not listed below. Only those AHRF variables in the abridged data set are included. Please see the AHRF user documentation for details on the other \~7000 variables (which includes data on county classifications, health professions, health facilities, utilization, expenditures, population, and environment)


### Identifying variables
| Data variable     | Description |  Source data set |
| ---   | --- | --- |
|**countyFIPS**| state-county FIPS Code | county_fips |
|**CountyName**| county name | county_fips |
|**StateName**| state abbreviation | county_fips |


### Data variables

#### Geographical identifiers
| Data variable     | Description | Source data set |
| ---   | --- | --- |
|**lat**| latitude corresponding to county's geographic center | county_latlong |
|**lon**| longitude corresponding to county's geographic center | county_latlong |
|CensusRegionName| name of census region | ahrf_health |
|CensusDivisionName| name of census division | ahrf_health |
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


#### Health Risk Factors

| Data variable     | Description | Source data set |
| ---   | --- | --- |
|**Smokers\_Percentage**| estimated percentage of adult smokers in county (2017) | chrr_smoking |
|SmokersLowCI95| lower limit of 95% confidence interval for adult smoking percentage | chrr_smoking |
|SmokersHighCI95| upper limit of 95% confidence interval for adult smoking percentage | chrr_smoking |
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
		

#### Social Distancing and Mobility (private data)
| Data variable     | Description | Source data set |
| ---   | --- | --- |
|**daily\_distance\_diff%Y-%m-%d**| change of average distance traveled on %Y-%m-%d from baseline (avg. distance traveled for same day of week during pre-COVID-19 time period for a specific county); dating from 2/24/20 to present-day (minus few days lag) | unacast_mobility |
|**daily\_visitation\_diff%Y-%m-%d**| change of visits to non-essential retail and services on %Y-%m-%d from baseline (avg. visits for same day of week during pre-COVID-19 time period for a specific county); dating from 2/24/20 to present-day (minus few days lag) | unacast_mobility |


#### Miscellaneous
| Data variable     | Description | Source data set |
| ---   | --- | --- |
|**dem\_to\_rep\_ratio**| ratio of the number of votes received by the Democratic candidate over that received by the Republican candidate in the 2016 presidential election | mit_voting |



