import sklearn
import copy
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from os.path import join as oj
import os
import matplotlib.dates as mdates
import seaborn as sns
# from viz import viz
from bokeh.plotting import figure, show, output_notebook, output_file, save
from functions import merge_data
from sklearn.model_selection import RandomizedSearchCV
from collections import Counter
import load_data
import naive_autoreg_baselines
import exponential_modeling
import pmdl_weight
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from functools import partial
import datetime
from shared_models import SharedModel
from collections import defaultdict 

very_important_vars = ['PopulationDensityperSqMile2010',
#                        'MedicareEnrollment,AgedTot2017',
                       'PopulationEstimate2018',
                       '#ICU_beds',
                       'MedianAge2010',
                       'Smokers_Percentage',
                       'DiabetesPercentage',
                       'HeartDiseaseMortality',
                        '#Hospitals']

exponential = {'model_type':'exponential'}
shared_exponential = {'model_type':'shared_exponential'}
demographics = {'model_type':'shared_exponential', 'demographic_vars':very_important_vars}


def fit_and_predict(df, 
                    outcome: str='deaths', 
                    method: str='exponential', 
                    mode: str='predict_future', 
                    target_day: np.ndarray=np.array([1]),
                    output_key: str=None,
                    demographic_vars=[],
                    verbose: bool=False):
    """
    Trains a method (method) to predict a current number of days ahead (target_day)
    Predicts the values of the number of deaths for the final day of test_df and writes to the column
    'predicted_deaths_'+method+'_'+str(target_day[-1]) of the test_df
    
    Params
    ------
    df
        a df with county level deaths and cases and demographic information
    outcome
        key for the outcome to predict (the values in this column should have a list for each row)
    method
        what method to use to do forecasting
    target_day
        np.array([1,2,..,n]) predicts these number of days ahead (can just be np.array([3])) for example if you just want 3 days ahead)
    output_key
        key to save the output as
    mode:
        either 'predict_future' or 'eval_mode'
        predict_future is predicting deaths on FUTURE days, so target_day=np.array([1])) means it predicts tomorrow's deaths
        eval_mode is for evaluating the performance of the classifier. 
        target_day=np.array([k])) will predict the current days death count using information from k days ago. 
        target_day= np.array([1,2,3,...,k]) will predict todays deaths, yesterdays deaths, deaths k-1 days ago using information from k days ago.


    Returns
    -------
    test_df
        returns dataframe with added column
    """
    assert mode == 'predict_future' or mode == 'eval_mode', 'unknown mode'
    if output_key is None:
        output_key = f'predicted_{outcome}_{method}_{target_day[-1]}'
        if len(demographic_vars) > 0:
            output_key += '_demographics'
    if method == 'AR':
        print('currently deprecated')
        raise NotImplementedError
        loss, model, best_window = naive_autoreg_baselines.train_and_evaluate_model(train_df,test_df)
        return naive_autoreg_baselines.make_predictions(test_df,model,best_window)
    
    elif method == 'exponential':
        preds = exponential_modeling.exponential_fit(df[outcome].values, 
                                                     mode=mode, 
                                                     target_day=target_day)
        
            
        df[output_key] = preds
        #del test_df['predicted_deaths_exponential']

        return df
    
    elif method == 'linear':
        preds = exponential_modeling.linear_fit(df[outcome].values, 
                                                     mode=mode, 
                                                     target_day=target_day)
        
            
        df[output_key] = preds
        #del test_df['predicted_deaths_exponential']

        return df        
    
    elif method == 'shared_exponential':
        # Fit a poisson GLM with shared parameters across counties. Input to the poisson GLM is demographic_vars and log(previous_days_deaths+1)
        cur_day_predictions = exponential_modeling.fit_and_predict_shared_exponential(df,mode,outcome=outcome,demographic_vars=demographic_vars,target_day=target_day, verbose=verbose)
        #if len(demographic_vars) > 0:
        #    output_key += '_demographics'
        # import IPython
        # IPython.embed()
        df[output_key] = cur_day_predictions
        return df
    
    elif method == 'ensemble':
        print('please use fit_and_predict_ensemble instead')

    elif method == 'advanced_shared_model':
        if 'neighbor_deaths' not in df.columns:
            neighboring_counties_df = pd.read_csv('../data_new/county_level/raw/county_ids/county_adjacency2010.csv')
            county_neighbor_deaths = []
            county_neighbor_cases = []
            county_fips = list(df['countyFIPS'])
            for fips in county_fips:


                neighboring_counties = list(neighboring_counties_df.loc[neighboring_counties_df['fipscounty'] == fips ]['fipsneighbor'])
                neighboring_county_deaths = list(df.loc[df['countyFIPS'].isin(neighboring_counties)]['deaths'])
                neighboring_county_cases = list(df.loc[df['countyFIPS'].isin(neighboring_counties)]['cases'])
                
                sum_neighboring_county_deaths = np.zeros(len(neighboring_county_deaths[0]))
                for deaths in neighboring_county_deaths:
                    sum_neighboring_county_deaths += deaths
                sum_neighboring_county_cases = np.zeros(len(neighboring_county_deaths[0]))
                for cases in neighboring_county_cases:
                    sum_neighboring_county_cases += cases
                county_neighbor_deaths.append(sum_neighboring_county_deaths)
                county_neighbor_cases.append(sum_neighboring_county_cases)


                    
            df['neighbor_deaths'] = county_neighbor_deaths
            df['neighbor_cases'] = county_neighbor_cases

    
    
    



        feat_transforms = defaultdict(lambda y: [lambda x: x]) 
        feat_transforms['deaths'] = [lambda x: np.log(x+1)]
        feat_transforms['cases'] =  [lambda x: np.log(x+1)]
        feat_transforms['neighbor_deaths'] =  [lambda x: np.log(x+1)]
        feat_transforms['neighbor_cases'] =  [lambda x: np.log(x+1)]
        default_values = defaultdict(lambda: 0) 
        aux_feats = ['cases','neighbor_deaths','neighbor_cases']
        shared_model = SharedModel(df=df,outcome=outcome,demographic_variables=[],mode=mode,target_days=target_day, feat_transforms=feat_transforms,auxiliary_time_features=aux_feats,time_series_default_values=default_values,scale=True)
        shared_model.create_dataset()
        shared_model.fit_model()
        shared_model.predict()

        df[output_key] = shared_model.predictions
        return df

        
        
    else:
        print('Unknown method')
        raise ValueError
        
        
def fit_and_predict_ensemble(df, 
                             target_day: np.ndarray=np.array([1]),
                             outcome: str='deaths', 
                             methods: list=[exponential, shared_exponential, demographics],
                             mode: str='predict_future', 
                             output_key: str=None,
                             verbose: bool=False):
    
    """
    Function for ensemble prediction
    Input:
        df: pd.DataFrame
        target_day: array
        outcome: str 
        method: list of dictionary
            each dictionary specify the type and parameters of the model
        mode: str
        output_key: str
    Output:
        df with ensemble prediction
    """
    if output_key is None:
        output_key = f'predicted_{outcome}_ensemble_{target_day[-1]}'
    predictions = {}
    for (i, model) in enumerate(methods):
        
        if 'demographic_vars' in model:
            demographic_vars = model['demographic_vars']
        else:
            demographic_vars = []
            
        predictions[i] = fit_and_predict(df, 
                                         outcome=outcome, 
                                         method=model['model_type'], 
                                         mode=mode, 
                                         target_day=target_day,
                                         output_key=f'y_preds_{i}',
                                         demographic_vars=demographic_vars,
                                         verbose=verbose)[f'y_preds_{i}'].values
            
    if mode == 'predict_future':
        use_df = df
    else:
        use_df = exponential_modeling.leave_t_day_out(df, target_day[-1])
            
    
    weights = pmdl_weight.compute_pmdl_weight(use_df, 
                                              methods=methods, 
                                              outcome=outcome,
                                              target_day=target_day)
    sum_weights = np.zeros(len(use_df))
    for model_index in weights:
        sum_weights = sum_weights + np.array(weights[model_index])
    
    #weighted_preds = np.zeros((len(use_df), len(target_day)))
    weighted_preds = [np.zeros(len(target_day)) for i in range(len(use_df))]
    for i in range(len(df)):
        for model_index in weights:
            weighted_preds[i] += np.array(predictions[model_index][i]) * weights[model_index][i] / sum_weights[i]

    # print out the relative contribution of each model
    if verbose:
        print('--- Model Contributions ---')
        model_weight_counter = Counter()
        for model_index in weights:
            m_weights = 0
            for i in range(len(use_df)):
                m_weights += weights[model_index][i] / sum_weights[i]
            m_weights = m_weights/len(use_df)
            model_weight_counter[model_index] = m_weights
        for model_index, weight in model_weight_counter.most_common():
            print(str(methods[model_index])+': '+str(weight))

    df[output_key] = weighted_preds
    return df
        

def get_forecasts(df,
                  outcome,
                  method,
                  output_key,
                  target_day=np.array([1]),
                  demographic_vars=[]
                  ):
    
    """
    This is a tentative interface for extracting cases/deaths forecasts of future days
    
    df: county_level df
    outcome: 'cases' or 'deaths'
    method: currently only support 'exponential' and 'shared_exponential'
    target_day:
    output_key
    
    output: df with forecasts in output_key 
    """
    
    ## not tested yet
    
    
    if method == 'exponential':
        return exponential_modeling.get_exponential_forecasts(df=df, 
                                                              outcome=outcome, 
                                                              target_day=target_day,
                                                              output_key=output_key)
         
    

    elif method == 'shared_exponential':
        df[output_key] = exponential_modeling.fit_and_predict_shared_exponential(df, 
                                                                                 mode='predict_future', 
                                                                                 demographic_vars=[],
                                                                                 outcome=outcome)
        return df
    elif method == 'shared_demographic':
        assert len(demographic_vars) > 0

        df[output_key] = exponential_modeling.fit_and_predict_shared_exponential(df, 
                                                                                 mode='predict_future', 
                                                                                 demographic_vars=demographic_vars,
                                                                                 outcome=outcome)
        return df
    
    elif method == 'ensemble':
        df[output_key] = fit_and_predict.fit_and_predict(df, 
                                                         method='ensemble',
                                                         mode='predict_future', 
                                                         demographic_vars=[],
                                                         outcome=outcome)[f'predicted_{outcome}_{method}_{target_day[-1]}']
        return df        

    
    else:
        print('Unknown method')
        raise ValueError        

        
        
def add_preds(df_county, NUM_DAYS_LIST=[1, 2, 3], verbose=False, cached_dir=None):
    # load cached preds
    if cached_dir is not None:
        # getting current date and time
        d = datetime.datetime.today()
        cached_fname = oj(cached_dir, f'preds_{d.month}_{d.day}_cached.pkl')
        
        if os.path.exists(cached_fname):
            return pd.read_pickle(cached_fname)
    
    print('predicting...')
    # df_county = exponential_modeling.estimate_deaths(df_county) # adds key 
    for num_days_in_future in NUM_DAYS_LIST: # 1 is tomorrow
        output_key = f'Predicted Deaths {num_days_in_future}-day'    
        df_county = fit_and_predict_ensemble(df_county, 
                                    # method='ensemble', 
                                    outcome='deaths',
                                    mode='predict_future',
                                    target_day=np.array([num_days_in_future]),
                                    output_key=output_key,
                                    verbose=verbose)

        # extract out vals from list
        if verbose:
            print(df_county.keys())
        vals = df_county[output_key].values
        out = []
        for i in range(vals.shape[0]):
            if np.isnan(vals[i]):
                out.append(0)
            else:
                out.append(vals[i][0])
        
        '''
        # set everything below 0.1 to 0.1
        out = np.array(out)
        out[out < 0.1] = 0.1
        '''
        
        df_county[output_key] = out
        
    if cached_dir is not None:
        df_county.to_pickle(cached_fname)
    return df_county