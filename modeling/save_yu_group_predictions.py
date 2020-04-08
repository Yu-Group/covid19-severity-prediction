import sys
sys.path.append('../') 
import sklearn
import copy
import numpy as np

import scipy as sp
import pandas as pd
from functions import merge_data
from sklearn.model_selection import RandomizedSearchCV
import load_data
import exponential_modeling


from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import fit_and_predict
from datetime import date

very_important_vars = ['PopulationDensityperSqMile2010',
#                        'MedicareEnrollment,AgedTot2017',
                       'PopulationEstimate2018',
                       '#ICU_beds',
                       'MedianAge2010',
                       'Smokers_Percentage',
                       'DiabetesPercentage',
                       'HeartDiseaseMortality',
                       'Respiratory Mortality',
                        '#Hospitals']
exponential = {'model_type':'exponential'}
shared_exponential = {'model_type':'shared_exponential'}
demographics = {'model_type':'shared_exponential', 'demographic_vars':very_important_vars}
linear = {'model_type':'linear'}

if __name__ == '__main__':

    df = load_data.load_county_level(data_dir = '../data/')
    max_cases = [max(v) for v in df['cases']]
    df['max_cases'] = max_cases
    df =  df[df['max_cases'] > 0]
    df = fit_and_predict.fit_and_predict_ensemble(df, 
                                                  target_day=np.array(range(1, 8)),
                                                  mode='predict_future',
                                                  outcome='deaths',
                                                  methods=[exponential, shared_exponential, demographics, linear],
                                                  output_key=f'predicted_deaths_ensemble_all'
                                                  )
    df = fit_and_predict.fit_and_predict_ensemble(df, 
                                                  target_day=np.array(range(1, 8)),
                                                  mode='predict_future',
                                                  outcome='deaths',
                                                  methods=[shared_exponential, demographics, linear],
                                                  output_key=f'predicted_deaths_ensemble_no_exponential_all'
                                                  )
    df = fit_and_predict.fit_and_predict_ensemble(df, 
                                                  target_day=np.array(range(1, 8)),
                                                  mode='predict_future',
                                                  outcome='deaths',
                                                  methods=[shared_exponential, linear],
                                                  output_key=f'predicted_deaths_ensemble_shared_linear_all'
                                                  )
    method_keys = [c for c in df if 'predicted' in c]
    for key in method_keys:
        for d in range(1, 8):
            newkey = key[:-3] + str(d)
            df[newkey] = np.array([p[d-1] for p in df[key].values])
    method_keys = [c for c in df if 'predicted' in c]
    geo = ['countyFIPS', 'CountyNamew/StateAbbrev']
    preds_df = df[method_keys + geo]
    today = date.today().strftime("%m/%d/%y").replace("/", "_")
    preds_df.to_csv(f"../predictions/predictions_{today}.csv")
    print("successfully uploaded predictions")
    
    