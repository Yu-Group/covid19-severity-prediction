#! /usr/bin/python3
import os
os.system("wget https://khn.org/wp-content/uploads/sites/2/2020/03/KHN-ICU-bed-county-analysis_2.zip -O khn_icu.zip")
os.system("unzip khn_icu.zip")
os.system("mv KHN_ICU_bed_county_analysis_2.xlsx khn_icu.xlsx")
os.system("mkdir DOC")
os.system("mv Read\ Me__KHN\ ICU\ bed\ county\ analysis.docx DOC/Readme_KHN.docx")
os.system("mv Terms\ of\ Use.pdf DOC/Terms\ of\ Use.pdf")
os.system("rm -f *.zip")