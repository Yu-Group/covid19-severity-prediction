import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_fips_df():
    url = "https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697"
    res = requests.get(url)
    html = res.text

    soup = BeautifulSoup(html, "lxml")
    table = soup.find_all("table", {"class": "data"})[0]
    trs = table.find_all("tr")

    oracleFIPS = {
        "countyFIPS": [],
        "state": [],
        "CountyName": []
    }

    for tr in trs:
        x = tr.find_all("td")
        if len(x) == 3:
            fips = str.lstrip(x[0].text)
            county = str.lstrip(x[1].text)
            state = str.lstrip(x[2].text)

            oracleFIPS["countyFIPS"].append(fips)
            oracleFIPS["state"].append(state)
            oracleFIPS["CountyName"].append(county)

    oracleFIPS = pd.DataFrame(oracleFIPS)
    return oracleFIPS