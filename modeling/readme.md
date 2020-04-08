# modeling docs

The model training and visualization pipeline lives in: `modeling/basic_model_framework.ipynb`
which will train and visualize the outputs of various models.

The high level wrapper for training and predicting values is the fit_and_predict function in `modeling/fit_and_predict.py`
this allows you to train a few models by passing in different arguments. For more details please see the function documentation.

# prediction

- To get deaths predictions of the naive exponential growth model, the simplest way is to call
```python
df = exponential_modeling.estimate_deaths(df, target_day=np.array([...]))

# df is county level dataFrame
# target_day: time horizon, target_day=np.array([1]) predicts the next day, target_day=np.array([1, 2, 3]) predicts next 3 days, etc.
# return: dataFrame with new column 'predicted_deaths_exponential' 
```