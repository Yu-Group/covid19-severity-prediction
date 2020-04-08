#! /usr/bin/python3
import os

os.system("mkdir state_data")

states_list = ['Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
              'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 
              'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 
              'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 
              'Nebraska', 'Nevada', 'New%20Hampshire', 'New%20Jersey', 'New%20Mexico', 
              'New%20York', 'North%20Carolina', 'Ohio', 'Oklahoma', 'Oregon', 
              'Pennsylvania', 'Rhode%20Island', 'South%20Carolina', 'South%20Dakota', 
              'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
              'West%20Virginia', 'Wisconsin', 'Wyoming', 'District%20of%20Columbia']

for state in states_list:
    os.system("wget https://www.countyhealthrankings.org/sites/default/files/media/document/2020%20County%20Health%20Rankings%20" + state + "%20Data%20-%20v1_0.xlsx -O ./state_data/chrr_health_" + state + ".xlsx")

states_list2 = ['Alabama', 'North%20Dakota']
for state in states_list2:
    os.system("wget https://www.countyhealthrankings.org/sites/default/files/media/document/2020%20County%20Health%20Rankings%20" + state + "%20Data%20-%20v1_1.xlsx -O ./state_data/chrr_health_" + state + ".xlsx")

states_list3 = ['West%20Virginia', 'Wyoming']
for state in states_list3:
    os.system("wget https://www.countyhealthrankings.org/sites/default/files/media/document/2020%20County%20Health%20Rankings%20" + state + "%20Data%20-%20v1.xlsx -O ./state_data/chrr_health_" + state + ".xlsx")