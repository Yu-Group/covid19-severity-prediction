#!/bin/bash

# The data is available at this webpage
# https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment/AcuteInpatientPPS/FY2020-IPPS-Final-Rule-Home-Page-Items/FY2020-IPPS-Final-Rule-Data-Files

wget https://www.cms.gov/Medicare/Medicare-Fee-for-Service-Payment/AcuteInpatientPPS/Downloads/FY2020-FR-Case-Mix-Index.zip
unzip -o -q FY2020-FR-Case-Mix-Index.zip
rm FY2020-FR-Case-Mix-Index.zip*
rm 'FY18 CMIs - V35 Billed DRGs (FR 2020).txt'
mv 'FY18 CMIs - V35 Billed DRGs (FR 2020).xlsx' 07_CMI_data.xlsx
