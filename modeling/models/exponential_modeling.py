import sklearn
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
# from viz import viz
from bokeh.plotting import figure, show, output_notebook, output_file, save
from functions import merge_data
from sklearn.model_selection import RandomizedSearchCV
from statsmodels.genmod.generalized_linear_model import PerfectSeparationError
from sklearn.preprocessing import StandardScaler
import load_data
import copy
import statsmodels.api as sm


def exponential_fit(counts, mode, target_day=np.array([1])): 
    # let target_day=np.array([5]) to predict 5 days in advance, 
    # and target_day=np.array([1, 2, 3, 4, 5]) to generate predictions for 1-5 days in advance 
    
    """
    Parameters:
        counts: array
            each row is the cases/deaths of one county over time
        target_day: array
            for each element {d} in the array, will predict cases/deaths {d} days from the last day in {counts}
    Return:
        array
        predicted cases/deaths for all county, for each day in target_day
    """
    predicted_counts = []
    for i in range(len(counts)):
        if mode == 'eval_mode':
            # Only use days up to from target[-1] for training. So if target[-1] = 1, only use the days before today for training and predict on today's data
            num_days_back = target_day[-1]
            train_ts = counts[i][:-num_days_back]
        elif mode == 'predict_future':
            # Use all days
            train_ts = counts[i]
        else:
            print('Unknown mode')
            raise ValueError 

        # if train_ts[-1] > 100:
        #     start = np.where(train_ts >= 10)[0][0]
        
        # elif train_ts[-1] >= 1:
        #     start = np.where(train_ts == 0)[0][-1] + 1
        # else:
        #     start = len(train_ts)
        # active_day = len(train_ts) - start # days since 'outbreak'


        # # active_day =5
        # # start = len(train_ts)-active_day 
        # if active_day > 5:
        #     active_day = 5
        #     start = len(train_ts) - active_day

        if train_ts[-1] >= 1:
             start = np.where(train_ts == 0)[0][-1] + 1
        else:
             start = len(train_ts)
        active_day = len(train_ts) - start # days since 'outbreak'
        if active_day > 5:
            active_day = 5 
        start = len(train_ts) - active_day
        
        if active_day <=2 or min(train_ts[start:]) == max(train_ts[start:]):
            # corner case 1: cases remain constant, unable to fit Poisson glm
            # solution: use previous day cases to predict
            predicted_counts.append(np.array([train_ts[-1]]*len(target_day)))
        #if active_day >= 3 and train_ts[-1] > 4:
        elif min(train_ts[start:]) > 0 and min(np.diff(np.log(train_ts[start:]))) == max(np.diff(np.log(train_ts[start:]))):
            # corner case 2: cases follow perfect exponential growth, unable to fit Poisson glm
            # solution: use cosntant growth rate to predict
            rate = 1.0 * train_ts[-1]/train_ts[-2]
            predicted_counts.append(np.array(train_ts[-1]*np.array([rate**i for i in target_day])))   
        else:
            # fit Poisson glm
            X_train = np.transpose(np.vstack((np.array(range(active_day)), 
                                              #np.log(np.array(range(active_day))+1),
                                              np.ones(active_day))))
            m = sm.GLM(train_ts[start:], 
                       X_train,
                       family=sm.families.Poisson(),
                       #family=sm.families.NegativeBinomial(alpha=.05),
                       freq_weights=np.array([1 ** i for i in range(active_day)])[::-1])
            try:
                m =  m.fit()
                X_test = np.transpose(np.vstack((target_day + active_day - 1, 
                                             #np.log(target_day + active_day),
                                             np.ones(len(target_day)))))
                predicted_counts.append(np.array(m.predict(X_test)))
            except PerfectSeparationError as e:
                print('Warning: PerfectSeparationError detected')
                rate = 1.0 * train_ts[-1]/train_ts[-2]
                predicted_counts.append(np.array(train_ts[-1]*np.array([rate**i for i in target_day])))  
                #X_train[-1][0] += 1
                #m = sm.GLM(train_ts[start:], 
                #X_train,
                #family=sm.families.Poisson(),
                #family=sm.families.NegativeBinomial(alpha=.05),
                #freq_weights=np.array([1 ** i for i in range(active_day)])[::-1])
                #m =  m.fit()

        #else:
        #    predicted_counts.append(np.array([train_ts[-1]]*len(target_day)))
            ## if there are too few data points to fit a curve, return the cases/deaths of current day as predictions for future

                
    return predicted_counts 




def estimate_cases(df, method="exponential", target_day=np.array([1]),
                   output_key='predicted_cases'):
    
    # estimate number of cases using exponential curve
    
    predicted_cases = []
    
    if method == "exponential":
        predicted_cases = exponential_fit(df['cases'].values, target_day=target_day)
    
    df[output_key] = predicted_cases
    return df
                
    
def linear_fit(counts, mode, target_day=np.array([1])): 
    # let target_day=np.array([5]) to predict 5 days in advance, 
    # and target_day=np.array([1, 2, 3, 4, 5]) to generate predictions for 1-5 days in advance 
    
    """
    Parameters:
        counts: array
            each row is the cases/deaths of one county over time
        target_day: array
            for each element {d} in the array, will predict cases/deaths {d} days from the last day in {counts}
    Return:
        array
        predicted cases/deaths for all county, for each day in target_day
    """
    predicted_counts = []
    for i in range(len(counts)):
        if mode == 'eval_mode':
            # Only use days up to from target[-1] for training. So if target[-1] = 1, only use the days before today for training and predict on today's data
            num_days_back = target_day[-1]
            train_ts = counts[i][:-num_days_back]
        elif mode == 'predict_future':
            # Use all days
            train_ts = counts[i]
        else:
            print('Unknown mode')
            raise ValueError 

        active_day = 4
        start = len(train_ts) - active_day
        
        if min(train_ts[start:]) == max(train_ts[start:]):
            # corner case 1: cases remain constant, unable to fit Poisson glm
            # solution: use previous day cases to predict
            predicted_counts.append(np.array([train_ts[-1]]*len(target_day)))
        elif min(np.diff(train_ts[start:])) == max(np.diff(train_ts[start:])):
            rate = max(train_ts[-1] - train_ts[-2], 0)
            predicted_counts.append(np.array(train_ts[-1] + np.array([rate*i for i in target_day])))            
        else:
            # fit Gaussian glm
            X_train = np.transpose(np.vstack((np.array(range(active_day)), 
                                              np.ones(active_day))))
            m = sm.GLM(train_ts[start:], 
                       X_train,
                       family=sm.families.Gaussian()
                       #family=sm.families.NegativeBinomial(alpha=.05),
                       )
            try:
                m = m.fit()
                X_test = np.transpose(np.vstack((target_day + active_day - 1, 
                                             np.ones(len(target_day)))))
                predicted_counts.append(np.array(m.predict(X_test)))
            except PerfectSeparationError as e:
                print('Warning: PerfectSeparationError detected')
                rate = max(train_ts[-1] - train_ts[-2], 0)
                predicted_counts.append(np.array(train_ts[-1] + np.array([rate*i for i in target_day])))  


        #else:
        #    predicted_counts.append(np.array([train_ts[-1]]*len(target_day)))
            ## if there are too few data points to fit a curve, return the cases/deaths of current day as predictions for future

                
    return predicted_counts 


def estimate_cases(df, method="exponential", target_day=np.array([1]),
                   output_key='predicted_cases'):
    
    # estimate number of cases using exponential curve
    
    predicted_cases = []
    
    if method == "exponential":
        predicted_cases = exponential_fit(df['cases'].values, target_day=target_day)
    
    df[output_key] = predicted_cases
    return df
    
def estimate_death_rate(df, method="constant"):
    
    predicted_death_rate = []
    
    if method == 'constant':
        for i in range(len(df)):
            predicted_death_rate.append(df['deaths'].values[i][-1]/max(1, df['cases'].values[i][-1]))
            
    df['predicted_death_rate'] = predicted_death_rate
    return df
    
    
def estimate_deaths(df, mode, method="exponential", 
                    target_day=np.array([1]),
                    output_key='predicted_deaths_exponential'):
    """
    mode: either 'predict_future' or 'eval_mode'
    predict_future is predicting deaths on FUTURE days, so target_day=np.array([1])) means it predicts tomorrow's deaths
    eval_mode is for evaluating the performance of the classifier. target_day=np.array([k])) will predict the current days death count
    using information from k days ago. target_day= np.array([1,2,3,...,k]) will predict todays deaths, yesterdays deaths, deaths k-1 days ago
    using information from k days ago.
    """
    
    predicted_deaths = []
    
    if method == 'exponential':
        predicted_deaths = exponential_fit(df['deaths'].values, mode, target_day=target_day)
        
    elif method == 'cases_exponential_rate_constant':
        print('Nick: I need to add eval/future mode')
        raise NotImplementedError
        
        # predicts number of cases using exponential fitting,
        # then multiply by latest death rate
        
        predicted_cases = estimate_cases(df, method="exponential", target_day=target_day)['predicted_cases'].values
        predicted_death_rate = estimate_death_rate(df, method="constant")['predicted_death_rate'].values
        predicted_deaths = [np.array(predicted_cases[i]) * predicted_death_rate[i] for i in range(len(df))]
        
    df[output_key] = predicted_deaths
        
    return df


def get_exponential_forecasts(df, 
                  outcome='cases',
                              
                  target_day=np.array([1]),
                  output_key='predicted_cases_exponential'):
    """
    merging cases and deaths prediction
    
    outcome='cases' for future cases prediction, 'deaths' for future deaths prediction
    """
    
    predicted_outcome = exponential_fit(df[outcome].values, mode='predict_future', target_day=target_day)
    df[output_key] = predicted_outcome
    
    return df
           
def leave_t_day_out(df, t):    
    df2 = copy.deepcopy(df)
    #days = len(df['deaths'].values[0])
    for i in range(len(df)):
        if 'deaths' in df2.columns:
             df2['deaths'].values[i] = df2['deaths'].values[i][:-t]
        if 'cases' in df2.columns:
            df2['cases'].values[i] = df2['cases'].values[i][:-t]
        if 'new_deaths' in df2.columns:
            df2['new_deaths'].values[i] = df2['new_deaths'].values[i][:-t]
        if 'deaths_per_cap' in df2.columns:
            df2['deaths_per_cap'].values[i] = df2['deaths_per_cap'].values[i][:-t]

        if 'neighbor_deaths' in df2.columns:
            df2['neighbor_deaths'].values[i] = df2['neighbor_deaths'].values[i][:-t]
            df2['neighbor_cases'].values[i] = df2['neighbor_cases'].values[i][:-t]
        
        if 'hospitalizations' in df2.columns:
            df2['hospitalizations'].values[i] = df2['hospitalizations'].values[i][:-t]

    return df2

def create_shared_simple_dataset(train_df, outcome='deaths',days_to_subtract=0):
    """
    Create a very simple dataset for creating a shared Poisson GLM across counties:
    Input: train_df: A df with county level deaths
    Output:
    X_train: a list of lists of the form [np.log(previous_days_death_count+1),1]
    y_train: a list of with elements - current_days_death_count
    """
    X_train = []
    y_train = []
    county_deaths = list(train_df[outcome])
    for i in range(len(county_deaths)):       
        deaths = county_deaths[i]
        for j in range(len(deaths)-days_to_subtract):
            # Only add a point if total death are greater than 3. (3 chosen abritrarily)
            if deaths[j] >= 3: 
                X_train.append([np.log(deaths[j-1]+1),1])
                y_train.append(deaths[j])
    return X_train, y_train


def create_time_features(time_index,county_deaths):
    time_feature_names = ['log(deaths)','dif log deaths']
    time_features = []
    time_features.append(np.log(county_deaths[time_index]+1))
    time_features.append(np.log(county_deaths[time_index]+1)-np.log(county_deaths[time_index-1]+1))
    return time_feature_names, time_features



def create_shared_demographic_dataset(train_df, demographic_vars, outcome='deaths',days_to_subtract=0):
    """
    Create a very simple dataset for creating a shared Poisson GLM across counties:
    Input: train_df: A df with county level deaths
    Output:
    X_train: a list of lists of the form [np.log(previous_days_death_count+1),1]
    y_train: a list of with elements - current_days_death_count
    """
    X_train = []
    y_train = []
    county_deaths = list(train_df[outcome])
    demographic_info = list(train_df[demographic_vars].values)
    for i in range(len(county_deaths)):       
        deaths = county_deaths[i]
        for j in range(len(deaths)-days_to_subtract):
            # Only add a point if total death are greater than 3. (3 chosen abritrarily)
            if deaths[j] >= 3: 
                # sometimes the numeric values are stored as strings for some variables
                demographics = [float(d) for d in list(demographic_info[i])]
                # time_feature_names, time_features = create_time_features(j-1,deaths)
                X_train.append(list(demographics)+[np.log(deaths[j-1]+1),1])
                y_train.append(deaths[j])
    return X_train, y_train



def _fit_shared_exponential(X_train,y_train):
    """
    Input: 
    X_train: A list of lists, where each sublist is [log(prev_days_death+1),1], where the 1 is for the bias term for the model
    y_train: A list of deaths for current day under the model
    Output: 
    Trains a poisson GLM with parameters shared across all counties.
    """

    model = sm.GLM(y_train, [x+[1] for x in X_train],
               family=sm.families.Poisson())

    # model = model.fit()
    model = model.fit_regularized()

    return model 


def fit_and_predict_shared_exponential(df,mode,outcome='deaths',demographic_vars=[],target_day=np.array([1]), verbose=False):
    """
    fits a poisson glm to all counties in train_df and makes prediction for the most recent day for test_df
    Input:
    df: dataframes with county level deaths, cases, and demographic information
    mode: either 'predict_future' or 'eval_mode'
    predict_future is predicting deaths on FUTURE days, so target_day=np.array([1])) means it predicts tomorrow's deaths
    eval_mode is for evaluating the performance of the classifier. target_day=np.array([k])) will predict the current days death count using info from k days ago
    demographic_vars: a list of columns to use for demographic variables
    Output:
    predicted_deaths: a list containing predictions for the current death count for current day of test_df
    """

    if len(demographic_vars) > 0:
        if mode == 'predict_future':
            X_train, y_train =  create_shared_demographic_dataset(df, demographic_vars, outcome=outcome)
        elif mode == 'eval_mode':
            X_train, y_train =  create_shared_demographic_dataset(df, demographic_vars, outcome=outcome,days_to_subtract=target_day[-1])
    else:
        if mode == 'predict_future':
            X_train, y_train =  create_shared_simple_dataset(df, outcome=outcome)
        elif mode == 'eval_mode':
            X_train, y_train =  create_shared_simple_dataset(df, outcome=outcome,days_to_subtract=target_day[-1])

    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)

    model = _fit_shared_exponential(X_train,y_train)
    features = demographic_vars+['log(deaths)','bias'] #,'bias2']
    if verbose:
        print('Feature weights')
        for i,f in enumerate(features):
            print(f+' : '+str(model.params[i]))

    predicted_deaths = get_shared_death_predictions(df,model,mode,target_day=target_day,outcome=outcome,demographic_vars=demographic_vars,scaler=scaler)
    return predicted_deaths


def _predict_shared_deaths(number_of_deaths,demographics,model,target_day,scaler):


    """
    Predicts deaths for days in target_day
    """
    # Inputs:
    # number_of_deaths: number of deaths to start predicting from
    # demographics: demographic information by county if any 
    # model: model that implements predict function
    # target_day: see parent functions
    death_predictions = [] 
    prev_deaths = number_of_deaths
    for i in range(target_day[-1]):
        cur_deaths = model.predict(scaler.transform([demographics+[np.log(prev_deaths+1),1]])+[1])[0]
        # cur_deaths = model.predict([demographics+[np.log(prev_deaths+1),1]+[1]])[0]

        if i+1 in target_day:
            death_predictions.append(cur_deaths)
        prev_deaths = cur_deaths
    return death_predictions




def get_shared_death_predictions(test_df,model,mode,target_day,scaler,outcome='deaths',demographic_vars=[]):
    """Predicts the death total for the most recent day in test_df
    Input:
    test_df: dataframes with county level deaths:
    Output:
    predicted_deaths: a list containing predictions for the current death count for current day of test_df
    """
    county_deaths = list(test_df[outcome])
    if len(demographic_vars) > 0:
        demographic_info =  list(test_df[demographic_vars].values)

    predicted_deaths = []
    for i,deaths in enumerate(county_deaths):
        if len(demographic_vars) > 0:
            # sometimes the numeric values are stored as strings for some variables
            demographics = [float(d) for d in list(demographic_info[i])]
        else:
            demographics = []
        if mode == 'predict_future':
            predicted_county_deaths = _predict_shared_deaths(deaths[-1],demographics,model,target_day,scaler)
        elif mode == 'eval_mode':
            predicted_county_deaths = _predict_shared_deaths(deaths[-(target_day[-1]+1)],demographics,model,target_day,scaler)
        predicted_deaths.append(predicted_county_deaths)

    return predicted_deaths 






