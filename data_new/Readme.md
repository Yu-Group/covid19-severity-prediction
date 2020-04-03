## Overview of all the data sets
- hospital level
    - cms_cmi: Case Mix Index for hospitals from CMS 
    - cms_hospitalpayment: Teaching Hospital info from CMS
    - DH_hospital: US Hospital info from Definitive Healthcase
    - hifld_hospital: Hospital info from homeland infrastructue foundation level data
- county level
    - data
## Folder Structure 
In this folder, we collect the useful hospital level data from a variety of sources. The strcture of the folder is as the following:
- raw (contains raw data)
    - [datasource]_[shortname]/
        - load.py (a script that loads the data)
        - download.py (a script that downloads the data)
        - raw data
        - Readme.md (metadata for the raw data)
- processed (contains the processed data)
    - [datasource]_[shortname]/
        - clean.py (a script that cleans the data)
        - cleaned data
        - Readme.md (metadata for the cleaned data)
