# Link updates every day and seems volatile (the current link is
# https://covid19-static.cdn-apple.com/covid19-mobility-data/2008HotfixDev26/v2/en-us/applemobilitytrends-2020-05-13.csv
# so we go through some extra steps to get the right url
from urllib.request import urlopen
from json import load
import os

BASE_PATH = "https://covid19-static.cdn-apple.com/"
response = load(urlopen("https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v2/index.json"))
CSV_PATH = BASE_PATH + response['basePath'] + response['regions']['en-us']['csvPath']
os.system(f"wget {CSV_PATH} -O apple.csv")