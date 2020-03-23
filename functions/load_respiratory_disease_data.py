import pandas as pd

def loadRespDiseaseSheet(sheet_name):
    filepath = "data/respiratory_disease/IHME_USA_COUNTY_RESP_DISEASE_MORTALITY_1980_2014_NATIONAL_Y2017M09D26.XLSX"
    orig_data = pd.read_excel(filepath,
                              sheet_name = "Chronic respiratory diseases",
                              skiprows = 1,
                              skipfooter = 2)
    orig_data = orig_data.dropna(subset = ["FIPS"])
    # omit the confidence intervals for now
    resp_mortality = orig_data['Mortality Rate, 2014*'].str.split(expand = True).iloc[:, 0]
    data = pd.DataFrame({'countyFIPS': orig_data['FIPS'].astype(int), 
                         'Respiratory Mortality': resp_mortality})
    return data