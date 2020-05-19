# Apple Maps Mobility Trends

- **Data source**: https://www.apple.com/covid19/mobility

- **Last downloaded**: updated daily

- **Data description**: uses data from Apple maps to report a relative (to January 13th, 2020)  volume of directions requests per country/region, sub-region or city

- **Known data quality issues**: 
	- Data for May 11-12 is not available and will appear as blank columns in the data set.

- **Short list of data columns**: (data in wide format)
	- **geo_type**: region type (country/region, city, sub-region)
    - **region**: name of region
    - **transportation_type**: type of transportation (driving, walking, transit) 
    - **alternative_name**: alternative name of region
    - **{DATE}**: social distancing measure for given date; a relative volume of directions requests per region compared to baseline volume on Jan 13, 2020

- **Notes**:
    - About this data (copied from https://www.apple.com/covid19/mobility): We define our day as midnight-to-midnight, Pacific time. Cities are defined as the greater metropolitan area and their geographic boundaries remain constant across the data set. In many countries/regions, sub-regions, and cities, relative volume has increased since January 13th, consistent with normal, seasonal usage of Apple Maps. Day of week effects are important to normalize as you use this data. Data that is sent from users’ devices to the Maps service is associated with random, rotating identifiers so Apple doesn’t have a profile of individual movements and searches. Apple Maps has no demographic information about our users, so we can’t make any statements about the representativeness of usage against the overall population.
    - For more on methodology, please see https://www.apple.com/covid19/mobility
