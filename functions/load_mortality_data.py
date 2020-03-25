import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

def loadMortalityData(suffix = ""):
    
    # get data path
    prefix = "./data/mortality/Compressed Mortality, 2012-2016"
    if suffix != "":
        suffix = ", " + suffix
        nrows = 3147
    else:
        nrows = 3143
    
    # original data is the sum over 5 years
    mortality = pd.read_table(prefix + suffix + ".txt", nrows = nrows, 
                              na_values = ["Suppressed", "Missing"])
    mortality = mortality.dropna(subset = ["Population"])
    
    # get yearly averages instead of 5yr sums
    mortality["Population"] = mortality["Population"] / 5
    mortality["Deaths"] = mortality["Deaths"] / 5
    mortality["MortalityRate"] = mortality.Deaths / mortality.Population * 1000
    
    # rename columns
    mortality = mortality.rename(columns = {'County Code': 'countyFIPS', 
                                            'Deaths': 'AllDeaths' + suffix,
                                            'MortalityRate': 'MortalityRate' + suffix})
    return mortality[["countyFIPS", "AllDeaths" + suffix, "MortalityRate" + suffix]]

def mergeMortalityData():
    mortality_merged = []
    
    suffixes = ["under20", "20-34", "35-54", "55-74", "over75"]
    for suffix in suffixes:
        mortality_add = loadMortalityData(suffix)
        if len(mortality_merged) == 0:
            mortality_merged = mortality_add
        else:
            mortality_merged = pd.merge(mortality_merged, mortality_add, on="countyFIPS")
    return mortality_merged