<h1> models </h1>
<div align="center"> <a type="button" class="btn btn-primary" style="margin-bottom: 30px; margin-right: 10px;" href="https://github.com/Yu-Group/covid19-severity-prediction/blob/master/modeling/readme.md">View modeling on Github</a> 
<a type="button" class="btn btn-info" style="margin-bottom: 30px;" href="https://github.com/Yu-Group/covid19-severity-prediction/predictions">cached predictions from different models</a></div>

We develop three Poisson regression-based models for predicting the trajectory of COVID-19-related deaths at
the county-level in the United States (updated daily). Our first model uses individual county death counts to forecast future deaths for that county;
our second model pools the death-count data across counties nation-wide to generate county-specific predictions that are informed by other counties across
the country; our third model uses an ensemble technique to combine predictions from the first two models, and can be viewed as adjusting a general
nation-wide model for individual county effects. The hope is that an understanding of the expected number of deaths will help guide necessary
county-specific decision-making and provide a realistic picture of the direction that we are heading.
Our models show that most counties are experiencing exponential growth that can be accurately modeled several days into the future.
However, we also find that some counties are starting to experience sub-exponential growth, possibly due to the
"flattening-the-curve" impacts of interventions such as social distancing and shelter in place orders. 

We also have developed some more models which adjust for demographics / risk factors (see details in the [paper]()). The plot below shows the accuracies for our 3-day predictions (predicting today from 3 days ago).

<figure class="video_container">
  <iframe src="https://yu-group.github.io/covid19-severity-prediction/results/predictions.html" frameborder="0" allowfullscreen="true" width="100%" height="800"> </iframe>
</figure>