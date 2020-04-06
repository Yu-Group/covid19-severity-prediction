# JHU Interventions (county-level) data set 

- **Data source**: https://github.com/JieYingWu/COVID-19_US_County-level_Summaries

- **Last downloaded**: downloaded directly from the GitHub source file

- **Data description**: contains the dates that counties (or states governing them) took measures to mitigate the spread by restricting gatherings, given as the proleptic Gregorian ordinal of the date, where January 1 of year 1 has t = 1. This convention is chosen for consistency with the python `datetime` library. A date in this format can be converted to year, month, date with:
```python
import datetime
date = datetime.date.fromordinal(ordinal_date)
print(date.month, date.day, date.year)
```

- **Known data quality issues**: n/a

- **Short list of data columns**: 
	- **countyFIPS**
	- **stay at home**
	- **>50 gatherings**
	- **>500 gatherings**
	- **public schools**
	- **restaurant dine-in**
	- **entertainment/gym**
	- **federal guidelines**
	- **foreign travel ban**

- **Notes**:
	- Please see sources and additional details [here](https://github.com/JieYingWu/COVID-19_US_County-level_Summaries/tree/master/data)
	- This interventions dataset is part of a larger corpus of data gathered by a group of students and faculty at Johns Hopkins University and is discussed in further detail in this [paper](https://arxiv.org/abs/2004.00756).