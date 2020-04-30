import numpy as np
import pandas as pd
from os.path import join as oj
import os
import pandas as pd
import sys
from scipy.stats import percentileofscore

def apply_manual_thresholds(vals, manual_thresholds = {3: 6,
                                                       2: 2,
                                                       1: 0}):
    new_col = vals * 0
    for key in sorted(manual_thresholds.keys()):
        new_col[vals >= manual_thresholds[key]] = key
    return new_col.astype(int)

def cut_with_manual_low(vals, LOW_THRESH=1):
    '''Everything below LOW_THRESH gets severity 1
    All other things are split evenly by percentile
    '''
    new_col = vals * 0
    new_col[vals < LOW_THRESH] = 1
    new_col[vals >= LOW_THRESH] = pd.qcut(vals[vals >= LOW_THRESH], 2, labels=False) + 2
    return new_col.astype(int)

def percentiles(vals):
    '''Map each value to its percentile
    '''
    new_col = vals * 0
    new_col = [percentileofscore(vals, v) for v in vals]
    return np.array(new_col).astype(int)

def cut_into_categories(vals, NUM_CATEGORIES=3):
    '''Evenly divide values into NUM_CATEGORIES categories
    (higher values get higher categories)
    '''
    return pd.qcut(vals, NUM_CATEGORIES, labels=False) + 1