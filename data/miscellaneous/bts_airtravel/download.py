#! /usr/bin/python3
import sys
import os
from os.path import join as oj
try:
    from google_drive_downloader import GoogleDriveDownloader as gdd
except ImportError:
    sys.exit("""You need googledrivedownloader.
                Install it from https://github.com/ndrplz/google-drive-downloader
                or run pip install googledrivedownloader.""")

os.mkdir('quarter_data')
gdd.download_file_from_google_drive(file_id='1kgFl9tMhce_vG7DzfKNCnviCcYc3nXZX', 
                                    dest_path=oj('quarter_data', 'bts_airtravel_q1.csv'))
gdd.download_file_from_google_drive(file_id='14XAxVTkAMKY85WRKiM8thnKfWJ_n4bcf', 
                                    dest_path=oj('quarter_data', 'bts_airtravel_q2.csv'))
gdd.download_file_from_google_drive(file_id='1sp6Sc8JnHUt6g1IaOdc06hz45kuao4v7', 
                                    dest_path=oj('quarter_data', 'bts_airtravel_q3.csv')) 
gdd.download_file_from_google_drive(file_id='1WIz940gyFvBQZ0YUMdd7Ams6Nd9YKhMh', 
                                    dest_path=oj('quarter_data', 'bts_airtravel_q4.csv'))