# ventilator demand prediction

[toc]


1. **Goal:** prioritizing where ventilators go
2. **Approach** 
    - predict ventilator demand + supply at the county-level 
    - filter hospitals and rank them according to their demand for additional ventilators
3. **Data** 
    - county-level: daily confirmed cases + deaths, demographics, comorbidity statistics, voting data, local gov. action data
    - hospital-level: information about hospitals (e.g. number of icu beds, hospital type, location)    
4. **Limitations**
    - currently using proxies for ventilator supply and demand instead of real measurements
    - limited data on bridging county-level data with hospital-level data


# 1 - goal: prioritizing where ventilators go

- working with [response4life](https://response4life.org/)
- would like to prioritize where to send available ventilators
- ideally, this would be where the ventilators could do the most "good" (e.g. save the most lives, minimize the Years of Life lost)

# 2 - approach

- begin by screening for large (academic) hospitals, which can accomodate more ventilators
- **outcomes**: we predict 2 things
    1. ventilator need - as a proxy for ventilator need, we predict the number of deaths (per county)
        - we estimate the ventilator need by scaling up the total number of expected deaths
        - here, we use many features at the county-level, such as demographics, comorbidity statistics, voting data
        - we are also trying to build in something local gov. action data (e.g. what has been enacted by local governments)
        - would like to use information directly from the hospital as well
        - this might also take into account some of the ventilator preparedness
    2. ventilator supply - as a proxy for current ventilator counts, we use the number of icu beds (per hospital)
        - in reality, there are more ventilators than icu beds
        - some ventilators (maybe 10-20%) will still be needed for non-covid-19 use
        - we would also like to build in something local gov. action data (e.g. what has been enacted by local governments)
        - would like to use information directly from the hospital as well
- using these outcomes, we then would like to prioritize different hospitals
    - still not sure how to combine them...
- these efforts should be coordinated with how the gov. is distributing ventilator stockpiles
- prediction setup
    - we restrict our analysis to counties which already have confirmed cases
    - each day, we randomly split counties to do prediction


# 3 - data

we have some data at the county-level and some at the hospital-level, which we jointly use to evaluate hospital need

## county-level data

- daily number of confirmed cases + deaths (from usafacts)
- population density, age distribution, gender distribution, presidential voting data, risk factors from medicare (e.g. diabetes, respiratory disease, ...), hospital data (e.g. # of doctors, # of hospitals, # of icu beds), and more demographic/disease data

## outbreak at the county-level
We can plot the outbreak for the counties with the highest number of deaths so far (updated daily):
<figure class="video_container" style="text-align: center">
  <iframe src="https://yu-group.github.io/covid-19-ventillator-demand-prediction/results/county_curves.html" frameborder="0" allowfullscreen="true" style="width:180%;height:1600px;"> </iframe>
</figure>

## interactive visualizations

We can visualize these features on interactive maps:
<figure class="video_container">
  <iframe src="https://yu-group.github.io/covid-19-ventillator-demand-prediction/results/NY.html" frameborder="0" allowfullscreen="true" style="width:150%;height:1600px;"> </iframe>
</figure>

## correlations between county-level features and number of deaths
Correlations with number of deaths

![](results/correlations.png)

## all correlations

Correlations between many different county-level features
![](results/correlations_heatmap.png)



## hospital-level data

- key predictors: icu beds, total staff, location info, ratings, hospital type
- some of this data is not public so we can't share it all here
- potentially contact information and more we are still merging in...