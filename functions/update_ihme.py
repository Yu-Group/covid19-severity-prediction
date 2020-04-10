import copy
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import zipfile, urllib.request, shutil
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
from os.path import join as oj
from datetime import datetime, timedelta
from os import listdir, path

# Constants
MAX_PROJECTION = 10
URL = 'https://ihmecovid19storage.blob.core.windows.net/latest/ihme-covid19.zip'
PROCESSED_DIREC = oj(currentdir, 'predictions', 'other_modeling', 'ihme/')
RAW_DIREC = oj(PROCESSED_DIREC, 'raw')

TWO_WEEKS, THREE_WEEKS = 14, 21
LOCATION = 'location_name' # keeps changing randomly from location to location_name


def unzip(path_to_zip_file, directory):
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory)

# Initialize file name
now = "".join(str(datetime.now())).replace(" ", "_")
file_name = oj(RAW_DIREC, now + '.zip')

# Download zip file
with urllib.request.urlopen(URL) as response, open(file_name, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)
        
# Unzip and delete zip file
unzip(file_name, RAW_DIREC)
os.remove(file_name)

def find_csvs( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith(suffix)]

def find_date(frame):
    # Find latest date for historical data
    dates = np.unique(frame[DATE])
    for date in dates[::-1]:
        delta = datetime.strptime(latest_date, '%Y-%m-%d') - datetime.strptime(date, '%Y-%m-%d')
        if abs(delta.days) <= 7:
            sub = frame.loc[frame[DATE] == date]
            sub = sub.loc[sub[LOCATION] == 'United States of America'].reset_index()
            current_date = True
            for i in range(sub.shape[0]):
                
                if sub['deaths_mean'].iloc[i] != sub['deaths_upper'].iloc[i]:
                    current_date = False
            
            if current_date:
                return date

# Get all downloaded directory names
directories = next(os.walk(RAW_DIREC))[1]
if '.ipynb_checkpoints' in directories:
    directories.remove('.ipynb_checkpoints')
    
# Find latest date
for i, directory in enumerate(directories):
    date = directory[:10].replace("_", '-')
    if i == 0:
        latest_date = date
        latest_direc = directory
    else:
        delta = datetime.strptime(date, '%Y-%m-%d') - datetime.strptime(latest_date, '%Y-%m-%d')
        if delta.days >= 0:
            latest_date = date
            latest_direc = directory
            
# Read main data file
csvs = find_csvs(oj(RAW_DIREC, latest_direc))
deaths = pd.read_csv(oj(RAW_DIREC, latest_direc, csvs[0]))

for col in list(deaths.columns):
    if 'location' in col:
        LOCATION = col
    elif 'date' in col:
        DATE = col
        
LATEST_DATE = find_date(copy.deepcopy(deaths))

# Columns for compiled data
columns = [LOCATION, DATE, 'totdea_mean', 'totdea_lower', 'totdea_upper', 'deaths_mean', 'deaths_lower', 'deaths_upper']
        
# Get unique locations
locations = np.unique(deaths[LOCATION])

for i, location in enumerate(locations):

    # Subset on lcoation
    sub_deaths = deaths.loc[deaths[LOCATION] == location]
    sub_deaths = sub_deaths.loc[sub_deaths[DATE] >= LATEST_DATE]

    sub_deaths = sub_deaths[columns].copy().reset_index()
    sub_deaths = sub_deaths.sort_values(by=DATE)

    # Calculate projections
    projections = pd.DataFrame([sub_deaths.iloc[0].values], columns=sub_deaths.columns)

    for j in range(1,MAX_PROJECTION+1):
        projections[str(j) + '_day_cumul_mean'] = sub_deaths.iloc[j]['totdea_mean']
        projections[str(j) + '_day_cumul_lower'] = sub_deaths.iloc[j]['totdea_lower']
        projections[str(j) + '_day_cumul_upper'] = sub_deaths.iloc[j]['totdea_upper']

        projections[str(j) + '_day_mean'] = sub_deaths.iloc[j]['deaths_mean']
        projections[str(j) + '_day_lower'] = sub_deaths.iloc[j]['deaths_lower']
        projections[str(j) + '_day_upper'] = sub_deaths.iloc[j]['deaths_upper']
        
    for j in [TWO_WEEKS,THREE_WEEKS]:
        projections[str(j) + '_day_cumul_mean'] = sub_deaths.iloc[j]['totdea_mean']
        projections[str(j) + '_day_cumul_lower'] = sub_deaths.iloc[j]['totdea_lower']
        projections[str(j) + '_day_cumul_upper'] = sub_deaths.iloc[j]['totdea_upper']

        projections[str(j) + '_day_mean'] = sub_deaths.iloc[j]['deaths_mean']
        projections[str(j) + '_day_lower'] = sub_deaths.iloc[j]['deaths_lower']
        projections[str(j) + '_day_upper'] = sub_deaths.iloc[j]['deaths_upper']

    if i == 0:
        compiled_projections = projections.copy()
    else:
        compiled_projections = compiled_projections.append(projections.copy(), ignore_index=True)

# Remove unnecessary columns
compiled_projections = compiled_projections.drop(columns=['index', 'totdea_upper', 'totdea_lower',
                                                         'deaths_upper', 'deaths_lower'])

# Rename column
compiled_projections = compiled_projections.rename(columns={"totdea_mean": "cumul_deaths",
                                                            "deaths_mean": 'deaths'})

# Change type to int
compiled_projections = compiled_projections.astype({'deaths': 'int32', 'cumul_deaths': 'int32'})

# Save to file
compiled_projections.to_csv(oj(PROCESSED_DIREC, LATEST_DATE + ".csv"), index = None)

print('sucesfully extracted IHME preds!')