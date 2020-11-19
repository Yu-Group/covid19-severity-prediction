# The New York Times and Dynata Mask-Wearing Survey Data (2020)

- **Data source**: https://github.com/nytimes/covid-19-data/tree/master/mask-use

- **Last downloaded**: downloaded directly from the GitHub source file

- **Data description**: This data, released by the NYT, contains the estimated prevalence of mask-wearing in counties in the US. Per the NYT, this data comes from a large number of interviews conducted online by the global data and survey firm Dynata at the request of The New York Times. The firm asked a question about mask use to obtain 250,000 survey responses between July 2 and July 14, enough data to provide estimates more detailed than the state level. (Several states have imposed new mask requirements since the completion of these interviews.)


- **Known data quality issues**: N/A

- **Short list of data columns**: 
	- **countyFIPS**: county FIPS
	- **Mask Never**: the estimated share of people in this county who would say never in response to the question “How often do you wear a mask in public when you expect to be within six feet of another person?”
	- **Mask Rarely**: the estimated share of people in this county who would say rarely
	- **Mask Sometimes**: the estimated share of people in this county who would say sometimes
	- **Mask Frequently**: the estimated share of people in this county who would say frequently
	- **Mask Always**: the estimated share of people in this county who would say always

- **Notes**:

	- For more details on the methodology, please see https://github.com/nytimes/covid-19-data/tree/master/mask-use
	- A nice article and graphic discussing the data and results: https://www.nytimes.com/interactive/2020/07/17/upshot/coronavirus-face-mask-map.html