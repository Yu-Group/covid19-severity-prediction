#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os

def load_medicare_chronic(data_dir='.'):
    ''' Load in CMS Chronic Conditions Data (2017)
    
    Parameters
    ----------
    data_dir : str; path to the data directory containing medicare_chronic.xlsx
    
    Returns
    -------
    data frame
    '''
    
    raw = pd.read_excel(oj(data_dir, "medicare_chronic.xlsx"), 
                        sheet_name = "All Beneficiaries", 
                        skiprows = 5, 
                        na_values = ["* ", "*", "  "])
    raw.columns = ["State", "County Name", "countyFIPS", "AlcoholAbuse", "Alzheimers", 
                   "Arthritis", "Asthma", "AtrialFibrillation", "Autism", "Cancer",
                   "KidneyDisease", "COPD", "Depression", "Diabetes", "DrugAbuse",
                   "HIVAIDS", "HertFailure", "Hepatitis", "Hyperlipidemia", 
                   "Hypertension", "Ischemic Heart Disease", "Osteoporosis", 
                   "Psychotic Disorders", "Stroke"]
    raw.columns = list(raw.columns)[:3] + ['Medicare' + col for col in list(raw.columns)[3:]]
    
    return raw

if __name__ == '__main__':
    raw = load_medicare_chronic()
    print('loaded medicare_chronic successfully.')
