#! /usr/bin/python3

import os

# download the fb social connectedness index data sets
if __name__ == '__main__':
    # country to country data
    os.system("wget https://data.humdata.org/dataset/e9988552-74e4-4ff4-943f-c782ac8bca87/resource/6265373e-c143-4d34-8786-641a13921173/download/country_country_aug2020.tsv")

    # county to country data
    os.system("wget https://data.humdata.org/dataset/e9988552-74e4-4ff4-943f-c782ac8bca87/resource/a9e327cc-d63f-4e61-b13d-d1968ee018bf/download/county_country_aug2020.tsv")

    # county to county data
    os.system("wget https://data.humdata.org/dataset/e9988552-74e4-4ff4-943f-c782ac8bca87/resource/3e3a1a7e-b557-4191-80cf-33d8e66c2e51/download/county_county_aug2020.tsv")

    # countries to sub-national regions data (gadm1-nuts2)
    os.system("wget https://data.humdata.org/dataset/e9988552-74e4-4ff4-943f-c782ac8bca87/resource/7570bcc3-a208-49c4-8821-17f8df93c0e2/download/gadm1_nuts2_gadm1_nuts2_aug2020.tsv")

    # countries to sub-national regions data (gadm1-nuts3)
    os.system("wget https://data.humdata.org/dataset/e9988552-74e4-4ff4-943f-c782ac8bca87/resource/3a98c06b-d373-45ed-a954-d93bdb12d5d0/download/gadm1_nuts3_counties_gadm1_nuts3_counties_aug2020.tsv.zip")
    os.system("unzip -nq gadm1_nuts3_counties_gadm1_nuts3_counties_aug2020.tsv.zip")
    os.system("rm gadm1_nuts3_counties_gadm1_nuts3_counties_aug2020.tsv.zip")


