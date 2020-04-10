# modeling docs

The model training and visualization pipeline lives in: `modeling/basic_model_framework.ipynb`
which will train and visualize the outputs of various models.

The high level wrapper for training and predicting values is the fit_and_predict function in `modeling/fit_and_predict.py`
this allows you to train a few models by passing in different arguments. For more details please see the function documentation.


To simply get the predictions for the best model, use the `add_preds` function:

```python
from fit_and_predict import add_preds
df = add_preds(df, NUM_DAYS_LIST=[1, 3, 5]) # adds keys like "Predicted Deaths 1-day", "Predicted Deaths 3-day"
# NUM_DAYS_LIST is list of number of days in the future to predict
```