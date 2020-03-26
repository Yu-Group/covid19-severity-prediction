import sklearn
import copy
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
import load_data

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

def make_auto_regressive_dataset(df,autoreg_window,log=True,deaths=True,cases=False,predict_deaths=True):
    """
    Make an autoregressive dataset that takes in a dataframe and a history window to predict number of deaths
    for a given day given a history of autoreg_window days before it
    log: take logarithm of values for features and predictions
    deaths: use number of previous deaths as features
    cases: use number of previous cases as features
    predict_deaths: predict deaths otherwise predict cases
    """

    assert (deaths == True or cases == True)
    feature_array = []
    ys = []
    _cases = list(df['cases'])
    _deaths = list(df['deaths'])
    for i in range(len(_cases)):
        for j in range(len(_cases[i])-(autoreg_window+1)):
            if predict_deaths:
                contains_event = sum(_deaths[i][j:j+autoreg_window+1]) > 0
            else:
                contains_event = sum(_cases[i][j:j+autoreg_window+1]) > 0
            if contains_event > 0:
                cases_window = _cases[i][j:j+autoreg_window]
                if log:
                    cases_window = [np.log(v+1) for v in cases_window ]
                deaths_window = _deaths[i][j:j+autoreg_window]
                if log:
                    deaths_window = [np.log(v+1) for v in deaths_window]
                if predict_deaths:
                    y_val = _deaths[i][j+autoreg_window+1]
                else:
                    y_val = _cases[i][j+autoreg_window+1]
                if log:
                    y_val = np.log(y_val+1)
                features = []
                if deaths == True:
                    features.extend(deaths_window)
                if cases == True:
                    features.extend(cases_window)
                feature_array.append(features)
                ys.append(y_val)
    return feature_array, ys          
    

def evaluate_model(model,eval_pair, metric, exponentiate=False):
    """
    Model: sklearn model
    Eval pair: (x,y)
    metric: sklearn metric
    exponentiate: exponentiate model predictions?
    """
    predictions = model.predict(eval_pair[0])
    y_val = eval_pair[1]
    if exponentiate:
        predictions = [np.exp(p) for p in predictions]
        y_val = [np.exp(y) for y in y_val]
    return predictions, metric(predictions,y_val)
    

def train_and_evaluate_model(train_df,test_df):
    model = sklearn.neighbors.KNeighborsRegressor()
    param_dist ={
        'n_neighbors': [2,4,8,16],
        'weights': ['uniform','distance'],
        'p': [1,2,4]
    }

    # model = RandomForestRegressor()
    # param_dist ={
    #     'n_estimators': [50,100,200,400,1000]
    # }
    # Number of randomly sampled hyperparams
    n_iter = 20
    metric = sklearn.metrics.mean_squared_error
    # n_jobs = number of cores to parallelize across
    random_search = RandomizedSearchCV(model, param_distributions=param_dist,
                                       n_iter=n_iter,n_jobs = 8)
    predict_deaths = False



    auto_reg_windows = [1,2,4,8]
    best_window = None
    best_loss = None
    for w in auto_reg_windows:
        log = False
        x_train, y_train = make_auto_regressive_dataset(train_df,w,log=log,predict_deaths=predict_deaths)
        x_test, y_test = make_auto_regressive_dataset(test_df,w,log=log,predict_deaths=predict_deaths)
        random_search.fit(x_train,y_train)
        window_loss = random_search.best_score_
        if best_loss is None:
            best_window = w
            best_loss = window_loss
        elif window_loss < best_loss:
            best_window = w
            best_score = window_loss



    x_train, y_train = make_auto_regressive_dataset(train_df,best_window,log=log)
    x_test, y_test = make_auto_regressive_dataset(test_df,best_window,log=log)
    random_search.fit(x_train,y_train)


    preds, loss = evaluate_model(random_search,(x_test,y_test),metric,exponentiate=True)
    
    return loss, random_search, best_window



def get_auto_reg_predictions(model,row,window,teacher_forcing=True,exponentiate=False,predict_deaths=True):
    if predict_deaths:
        key = 'deaths'
    else:
        key = 'cases'

    deaths = row[key]
    predictions = [0]*window 
    if teacher_forcing:
        for i in range(len(deaths)-(window)):
            x = deaths[i:i+window]
            cur_prediction = model.predict([x])
            if exponentiate:
                cur_prediction = np.exp(cur_prediction)
            predictions.append(cur_prediction)
    else:
        raise NotImplementedError
    return predictions


def make_predictions(df,model,window):
    # WARNING: does not yet supported number of previous cases as feature
    predictions_list = []
    for i in range(len(df)):
        row = df.iloc[i]
        cur_preds = get_auto_reg_predictions(model,row,window)
        predictions_list.append(cur_preds)
    df['predicted_deaths'] = predictions_list
    return df


def fit_and_predict(train_df,test_df):
    loss, model, best_window = train_and_evaluate_model(train_df,test_df)
    return make_predictions(test_df,model,best_window)

