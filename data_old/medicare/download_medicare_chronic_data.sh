#!/bin/bash
wget https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Chronic-Conditions/Downloads/CC_Prev_State_County_Age.zip -O 01_medicare_chronic_data.zip
unzip 01_medicare_chronic_data.zip

# remove unneccesary files
rm -f *.zip
rm -f County_Table_Chronic_Conditions_Prevalence_by_Age_200{7..9}.xlsx
rm -f County_Table_Chronic_Conditions_Prevalence_by_Age_201{0..6}.xlsx