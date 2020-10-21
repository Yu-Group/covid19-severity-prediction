# Facebook Social Connectedness Index Data (2020)

- **Data source**: https://data.humdata.org/dataset/social-connectedness-index

- **Last downloaded**: 10/20/2020

- **Data description**: An anonymized snapshot of all active Facebook users and their friendship networks to measure the intensity of connectedness between locations. The Social Connectedness Index (SCI) is a measure of the social connectedness between different geographies (i.e., country to country, county to country, county to county, sub-national regions to sub-national regions). Specifically, it measures the relative probability that two individuals across two locations are friends with each other on Facebook.

- **Known data quality issues**: n/a

- **Data columns**: (cleaned data)
	- **Location1**: First location (can be country, county FIPS, or sub-national regions depending on the specified level of granularity)
	- **Location2**: Second location (can be country, county FIPS, or sub-national regions depending on the specified level of granularity)
	- **SCI**: social connectedness index between Location1 and Location2 based upon Facebook friendship networks

- **Notes**: 
	- This data can be downloaded in multiple granularities: "country_country", "county_country", "county_county", "gadm1_nuts2", "gadm1_nuts3"
	- Detailed documentation about the data, these different levels, and the SCI can be found [here](https://data.humdata.org/dataset/e9988552-74e4-4ff4-943f-c782ac8bca87/resource/a0c37eb4-b45c-436d-b2b2-c0c9b1974318/download/facebook-social-connectedness-index-data-notes.pdf)
	- An exploratory paper using this data:
	Kuchler, Theresa, Dominic Russel, and Johannes Stroebel. The geographic spread of COVID-19 correlates with structure of social networks as measured by Facebook. No. w26990. National Bureau of Economic Research, 2020. [(Link)](http://pages.stern.nyu.edu/~jstroebe/PDF/SCI_and_COVID.pdf)




