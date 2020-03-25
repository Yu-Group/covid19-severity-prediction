import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

def loadMortalityData():
    # original data is the sum over 5 years
    mortality = pd.read_table("./data/mortality/Compressed Mortality, 2012-2016.txt", 
                              nrows = 3143)
    
    # get yearly averages instead of 5yr sums
    mortality["Population"] = mortality["Population"] / 5
    mortality["Deaths"] = mortality["Deaths"] / 5
    mortality["MortalityRate"] = mortality.Deaths / mortality.Population * 1000
    
    # rename columns
    mortality = mortality.rename(columns = {'County Code':'countyFIPS', 'Deaths': 'AllDeaths'})
    return mortality[["countyFIPS", "AllDeaths", "MortalityRate"]]