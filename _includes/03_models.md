<h1> models </h1>
<div align="center"> <a type="button" class="btn btn-primary" style="margin-bottom: 30px; margin-right: 10px;" href="https://github.com/Yu-Group/covid19-severity-prediction/blob/master/modeling/readme.md">View modeling on Github</a> 
</div>

<img src="results/models.jpg" style="width:100%;">
<p style="text-align: center; font-size: x-large;">Combined Linear and Exponential Predictors (CLEP) </p>
<p style="text-align: center; font-size: large;">Calculate a <strong>weighted average of the predictions</strong>: higher weight to the models with better historical performance</p>

We develop simple, interpretable models for predicting the trajectory of COVID-19-related deaths at
the county-level in the United States (updated daily). Our models show that most counties are experiencing exponential growth that can be accurately modeled several days into the future.
However, we also find that some counties are starting to experience sub-exponential growth, possibly due to the
"flattening-the-curve" impacts of interventions such as social distancing and shelter in place orders. Details are in our [paper](https://arxiv.org/abs/2005.07882).

<img src="results/forecasts.svg" style="width:100%;">
**5-day forecasts for selected counties**: Prediction intervals are based on the historical performance of our predictors (narrower for counties where the forecasts were accurate). If we denote *err* as the largest normalized absolute error for a given county in the past five days, then our prediction interval has the form \[prediction * (1 - *err*), prediction * (1 + *err*)\].

<figure class="video_container">
  <iframe src="results/predictions.html" frameborder="0" allowfullscreen="true" width="100%" height="650px"> </iframe>
</figure>
**Predictive accuracy**: Accuracy of our 3-day predictions (predicting today from 3 days ago). Bubble size corresponds to county size (this plot omits counties which have no recorded deaths as of today).

