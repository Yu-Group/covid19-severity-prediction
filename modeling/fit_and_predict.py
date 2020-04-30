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
import inspect
import sys
from tqdm import tqdm

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


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
linear = {'model_type':'linear'}
advanced_model = {'model_type':'advanced_shared_model'}


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
        

    
    
    



        feat_transforms = defaultdict(lambda y: [lambda x: x]) 
        feat_transforms['deaths_per_cap'] = [lambda x: np.log(x+1)]
        feat_transforms['deaths'] = [lambda x: np.log(x+1)]
        feat_transforms['new_deaths'] = [lambda x: np.log(x+1)]
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
                             methods: list=[shared_exponential, linear],
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
        
        
def previous_prediction_errors(df, 
                               target_day: np.ndarray=np.array([1]),
                               outcome: str='deaths', 
                               methods: list=[advanced_model, linear],
                               look_back_day: int=5,
                               output_key: str=None):
    """
    Calculating prediction errors of previous days
    Input:
        df: pd.DataFrame
        target_day: np.ndarray
        outcome: str
        methods: list
        look_back_day: int
            returns the prediction errors for the last {look_back_day} days
    Output:
        list of {len(df)} dictionaries, the keys of each dictionary are days in target_day, and the values are a list of (normalized) l1 error, of length {look_back_day}
    """
    
    # find previous models to run
    previous_start_days = defaultdict(list)
    for day in target_day:
        for back_day in range(look_back_day):
            previous_start_days[day + back_day].append(day)
    
    #previous_model_predictions = {}
    previous_model_errors = [defaultdict(list) for i in range(len(df))]
    prediction_uncertainty = [defaultdict(list) for i in range(len(df))]
    
    for t in previous_start_days:
        
        previous_target_days = previous_start_days[t]
        df_old = exponential_modeling.leave_t_day_out(df, t)
        
        previous_model_predictions = fit_and_predict_ensemble(df_old, 
                                             target_day=np.array(previous_target_days),
                                             outcome=outcome, 
                                             methods=methods,
                                             mode='predict_future', 
                                             output_key='old_predictions',
                                             )['old_predictions'].values # running old prediction models
        for i in range(len(df)):
            for (j, td) in enumerate(previous_target_days):
                pred = previous_model_predictions[i][j]
                actual_outcome = df[outcome].iloc[i][td-t-1]
                error = actual_outcome/max(pred, 1)-1
                previous_model_errors[i][td].append(error)
        
    #for i in range(len(df)):
    #    for td in target_day:
     #       prediction_uncertainty[i][td] = max(previous_model_errors[i][td])
    
    df[output_key] = previous_model_errors
            
    return df


def add_prediction_intervals(df, 
                             target_day: np.ndarray=np.array([1]),
                             outcome: str='deaths', 
                             methods: list=[advanced_model, linear],
                             interval_type: str='local',
                             look_back_day: int=5,
                             output_key: str=None):
    """
    Adding intervals for future prediction
    Input:
        df: pd.DataFrame
        target_day: np.ndarray
        outcome: str
        methods: list
        interval_type: str
            'local' or 'combined'
    Output:
        list of {len(df)} dictionaries, the keys of each dictionary are days in target_day, and the values are the predicted intervals
     """
    
    assert interval_type == 'local' or interval_type == 'combined', 'unknown interval type'
    lower_bound = {'deaths':10, 'cases':10}
    
    df = previous_prediction_errors(df, target_day, outcome, methods, look_back_day=5, output_key='previous_errors')
    
    df = fit_and_predict_ensemble(df, 
                                  target_day=target_day,
                                  outcome=outcome, 
                                  methods=methods,
                                  mode='predict_future', 
                                  output_key='new_predictions',
                                  verbose=False)
    
    preds = df['new_predictions'].values
    latest_cases = np.array([p[-1] for p in df[outcome].values])
    intervals = [[] for i in range(len(df))]
    qts = {}
    for td in target_day:
        all_errors = []
        for i in range(len(df)):
            if latest_cases[i] >= lower_bound[outcome]:
                all_errors += df['previous_errors'].values[i][td]
        qts[td] = (np.quantile(np.array(all_errors), .05), np.quantile(np.array(all_errors), .95))
    
    for i in range(len(df)):
        largest_error = []
        for (j, td) in enumerate(target_day):
            largest_error.append(max(np.abs(np.array(df['previous_errors'].values[i][td]))))
            if interval_type == 'local':
                intervals[i].append((max(preds[i][j]*(1 - largest_error[-1]), latest_cases[i]), 
                                     preds[i][j]*(1 + largest_error[-1])))
            elif interval_type == 'combined':
                intervals[i].append((max(preds[i][j]*(1 + (qts[td][0] - largest_error[-1])/2), latest_cases[i]), 
                                     preds[i][j]*(1 + (largest_error[-1] + qts[td][1])/2)))                  
    df[output_key] = intervals
    return df

        
def add_preds(df_county, NUM_DAYS_LIST=[1, 2, 3], verbose=False, cached_dir=None,
              outcomes=['Deaths', 'Cases']):
    '''Adds predictions for the current best model
    Adds keys that look like 'Predicted Deaths 1-day', 'Predicted Deaths 2-day', ...
    '''
    
    # select the best model
    advanced_model = {'model_type':'advanced_shared_model'}
    linear = {'model_type':'linear'}
    BEST_MODEL = [advanced_model, linear]
    
    
    # load cached preds
    if cached_dir is not None:
        # getting current date and time
        d = datetime.datetime.today()
        cached_fname = oj(cached_dir, f'preds_{d.month}_{d.day}_cached.pkl')
        
        if os.path.exists(cached_fname):
            return pd.read_pickle(cached_fname)
    
    print('predictions not cached, now calculating (might take a while)')
    for outcome in outcomes:
        print(f'predicting {outcome}...')
        for num_days_in_future in tqdm(NUM_DAYS_LIST): # 1 is tomorrow
            output_key = f'Predicted {outcome} {num_days_in_future}-day'    
            df_county = fit_and_predict_ensemble(df_county, 
                                        methods=BEST_MODEL,
                                        outcome=outcome.lower(),
                                        mode='predict_future',
                                        target_day=np.array([num_days_in_future]),
                                        output_key=output_key,
                                        verbose=verbose)

            vals = df_county[output_key].values
            out = []
            for i in range(vals.shape[0]):
                if np.isnan(vals[i]):
                    out.append(0)
                else:
                    out.append(max(vals[i][0],
                                   list(df_county[outcome.lower()])[i][-1]))
            df_county[output_key] = out
            
            
        output_key = f'Predicted {outcome} Intervals'    
        print('prediction intervals...')
        df_county = add_prediction_intervals(df_county, 
                             target_day=np.array(NUM_DAYS_LIST),
                             outcome=outcome.lower(), 
                             methods=BEST_MODEL,
                             interval_type='local',
                             output_key=output_key)
        
    # add 3-day lagged death preds
    output_key = f'Predicted Deaths 3-day Lagged'
    df_county = fit_and_predict_ensemble(df_county, 
                                methods=BEST_MODEL,
                                outcome='deaths',
                                mode='eval_mode',
                                target_day=np.array([3]),
                                output_key=output_key,
                                verbose=verbose)
    df_county[output_key] = [v[0] for v in df_county[output_key].values]
    
    
    if cached_dir is not None:
        df_county.to_pickle(cached_fname)
    return df_county



def tune_hyperparams(df,target_day,outcome,output_key,method_hyperparam_dict,error_fn,num_iters):

    def fit_model_with_random_params(df,i):
        output_key = 'hyperparams_i'
        methods = []
        for method_name in method_hyperparam_dict:
            method_dict = {}
            method_dict['model_type'] = method_name
            method_hyperparam_choices = method_hyperparam_dict[method_name]
            for param_name in method_hyperparam_choices:
                method_dict[param_name] = random.choice(method_hyperparam_choices[param_name])
            methods.append(method_dict)
        fit_and_predict_ensemble(df=df, target_day=target_day, outcome=outcome, methods=methods, 
                                 mode='eval_mode', output_key=output_key)

        score = error_fn(df[output_key],df['outcome'])
        return params, score

    results = Counter()
    for i in range(num_iters):
        params, score = fit_model_with_random_params(copy.deepcopy(df),i)
        results[params] = -1*score

    best_param, value = results.most_common()


    return best_param, -1*value

