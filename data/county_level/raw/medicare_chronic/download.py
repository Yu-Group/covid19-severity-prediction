#! /usr/bin/python
import os
os.system("wget https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Chronic-Conditions/Downloads/CC_Prev_State_County_Age.zip -O medicare_chronic_raw.zip")
os.system("unzip medicare_chronic_raw.zip")
os.system("mv County_Table_Chronic_Conditions_Prevalence_by_Age_2017.xlsx medicare_chronic.xlsx")

# remove unneccesary files
os.system("rm -f *.zip")
os.system("rm -f County_Table_Chronic_Conditions_Prevalence_by_Age_200{7..9}.xlsx")
os.system("rm -f County_Table_Chronic_Conditions_Prevalence_by_Age_201{0..6}.xlsx")