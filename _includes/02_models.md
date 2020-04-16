<h1> models </h1>
<div align="center"> <a type="button" class="btn btn-primary" style="margin-bottom: 30px; margin-right: 10px;" href="https://github.com/Yu-Group/covid19-severity-prediction/blob/master/modeling/readme.md">View modeling on Github</a> 
</div>

<img src="https://yu-group.github.io/covid19-severity-prediction/results/models.png" style="width:100%;">
**Models**: We develop simple, interpretable models for predicting the trajectory of COVID-19-related deaths at
the county-level in the United States (updated daily). Our models show that most counties are experiencing exponential growth that can be accurately modeled several days into the future.
However, we also find that some counties are starting to experience sub-exponential growth, possibly due to the
"flattening-the-curve" impacts of interventions such as social distancing and shelter in place orders. Details are in the [paper](https://www.stat.berkeley.edu/~binyu/ps/papers2020/covid19_paper.pdf).

<figure class="video_container">
  <iframe src="https://yu-group.github.io/covid19-severity-prediction/results/predictions.html" frameborder="0" allowfullscreen="true" width="100%" height="650px"> </iframe>
</figure>
**Predictive accuracy**: This scatterplot shows the accuracy of our 3-day predictions (predicting today from 3 days ago). Bubble size corresponds to county size.

