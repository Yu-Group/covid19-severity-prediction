#! /usr/bin/python3
import pandas as pd
import os

try:
    from sas7bdat import SAS7BDAT
except ImportError:
    sys.exit("""You need sas7bdat.
                Install it from https://pypi.org/project/sas7bdat/
                or run pip install sas7bdat.""")
    
import AHRF_parser

# download raw data files
os.system("wget https://data.hrsa.gov//DataDownload/AHRF/AHRF_2018-2019_SAS.zip -O ahrf_raw_sas.zip")
os.system("unzip -nq ahrf_raw_sas.zip")
os.system("wget https://data.hrsa.gov//DataDownload/AHRF/AHRF_2018-2019.ZIP -O ahrf_raw.zip")
os.system("unzip -nq ahrf_raw.zip")

# sas7bdat to data frame
with SAS7BDAT('ahrf2019.sas7bdat', skip_header=False) as reader:
	df = reader.to_data_frame()

# generate meta_data.csv
if not os.path.exists("./DOC/meta_data.csv"):
   ahrf_parser = AHRF_parser.parse_AHRF_ascii(num_cores = 1, 
                                              ascii_file_path = "./DATA/AHRF2019.asc", 
                                              sas_file_path = "./DOC/AHRF2018-19.sas")

# rename features
meta = pd.read_csv('./DOC/meta_data.csv')
meta_dict = {}
for i in range(meta.shape[0]):
    r = meta.iloc[i]
    meta_dict[r.FieldId] = r.FieldName
df = df.rename(columns = meta_dict)

df.to_csv("ahrf_health.csv", header=True, index=False)

# remove unnecessary files
os.system("rm -f *.zip")
os.system("rm -r DATA")
os.system("rm 2018-2019_AHRFDUA.doc ahrf2019.sas7bdat DOC/AHRF2018-19.sas")
