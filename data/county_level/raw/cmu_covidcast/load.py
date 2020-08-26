#!/usr/bin/python3

import pandas as pd
from os.path import join as oj
import os
import covidcast
from datetime import date

def load_cmu_covidcast(data_dir='.'):
    ''' Load in CMU COVIDcast (county-level) data set (pulled directly from source)
    
    Parameters
    ----------
    data_dir : str; path to the data directory to write raw cmu_covidcast.csv
    
    Returns
    -------
    data frame
    '''
    
    signals_ls = []
    
    signal_dict = {
#         "safegraph": ["full_time_work_prop", "part_time_work_prop", "completely_home_prop", "median_home_dwell_time"],
        "fb-survey": ["smoothed_hh_cmnty_cli", "smoothed_cli"],
        "doctor-visits": ["smoothed_adj_cli"],
        "hospital-admissions": ["smoothed_adj_covid19"],
        "indicator-combination": ["nmf_day_doc_fbc_fbs_ght"]
    }
    
    print("Loading CMU signals:")
    for source, signals in signal_dict.items():
        for signal in signals:
            print(source + " " + signal)
            signals_ls.append(covidcast.signal(source, signal, geo_type="county").rename(columns = {
                "geo_value": "countyFIPS",
                "time_value": "date",
                "value": source + "-" + signal
            }).drop(columns = ["direction", "issue", "lag", "stderr", "sample_size"]))
    
    for i in range(len(signals_ls)):
        if i == 0:
            raw = signals_ls[i]
        else:
            raw = pd.merge(raw, signals_ls[i], on=['countyFIPS', 'date'], how="outer")  # merge data
    raw = raw.sort_values("date")
    raw.to_csv(oj(data_dir, "cmu_covidcast.csv"), header=True, index=False)

    return raw

if __name__ == '__main__':
    raw = load_cmu_covidcast()
    print('loaded cmu_covidcast successfully.')



