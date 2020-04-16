#!/usr/bin/python3

import os

os.system("wget https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment/AcuteInpatientPPS/Downloads/FY2020-FR-Case-Mix-Index.zip")
os.system("unzip -o -q FY2020-FR-Case-Mix-Index.zip")
os.system("rm FY2020-FR-Case-Mix-Index.zip*")
os.system("rm 'FY18 CMIs - V35 Billed DRGs (FR 2020).txt'")
os.system("mv 'FY18 CMIs - V35 Billed DRGs (FR 2020).xlsx' cms_cmi.xlsx")
