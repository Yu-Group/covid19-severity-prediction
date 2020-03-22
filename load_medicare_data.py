import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

def loadChronicSheet(sheet_name):
    orig_data = pd.read_excel("data/County_Table_Chronic_Conditions_Prevalence_by_Age_2017.xlsx",
                              sheet_name = sheet_name,
                              skiprows = 5,
                              na_values = ["* ", "*", "  "])
    orig_data.columns = ["State", "County", "countyFIPS", "Alcohol Abuse", "Alzheimers", 
                         "Arthritis", "Asthma", "Atrial Fibrillation", "Autism", "Cancer",
                         "Kidney Disease", "COPD", "Depression", "Diabetes", "Drug Abuse",
                         "HIV/AIDS", "Heart Failure", "Hepatitis", "Hyperlipidemia", 
                         "Hypertension", "Ischemic Heart Disease", "Osteoporosis", 
                         "Psychotic Disorders", "Stroke"]
    orig_data.columns = list(orig_data.columns[:3]) + ["condition_" + name for name in orig_data.columns[3:]]
    orig_data = orig_data.dropna(subset = ["County"])
    return orig_data