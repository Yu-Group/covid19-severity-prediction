import numpy as np 
import pandas as pd

class MovingAverage:
    def __init__(self, df, outcome, target_days=np.array([5])):
        self.df = df
        self.outcome = outcome
        self.target_days = target_days[0] # Just take the first one for now
        
    def predict(self, window=5):
        moving_average = []
        outcomes = self.df[self.outcome].values
        outcomes = np.stack(outcomes) # Flatten to get matrix
        for i in range(0, len(self.df)):
            ts = outcomes[i,:]

#             Assert that we have a long enough array
            try: 
                assert len(ts) >= window
            except:
                a = 1
                #print("Array length too small for given window size. Please pass larger array or lower window.")
                
                
         
            ts_cp = np.array(ts, dtype=float)
            

            for j in range(0, self.target_days):
                pred_ma = np.mean(ts_cp[-window:])
                ts_cp = np.append(ts_cp, pred_ma)

            moving_average.append([ts_cp[-1]])
            
        self.predictions = moving_average
            

            
## TESTS

# Test 3 day out prediction
def moving_average_test():
    true = [3.6799999999999997, 12.68]
    ## Create Fake Data
    dicti = {
        "hosp": ["1", "2"],
        "hospitalizations": [np.array([1,2,3,4,5]), np.array([10, 11, 12, 13, 14])]
    }
    
    df = pd.DataFrame(dicti)
    
    ma = MovingAverage(df, outcome="hospitalizations", target_days=np.array([3]))
    ma.predict()
    
    for i in range(0, len(true)):
        assert true[i] == ma.predictions[i][0]
        
def moving_average_test_pred():
    true = [3.6799999999999997, 12.68]
    ## Create Fake Data
    dicti = {
        "hosp": ["1", "2"],
        "hospitalizations": [np.array([1,2,3,4,5]), np.array([10, 11, 12, 13, 14])]
    }
    
    df = pd.DataFrame(dicti)
    
    ma = MovingAverage(df, outcome="hospitalizations", target_days=np.array([3]))
    ma.predict()
    
    df["preds"] = ma.predictions
    return df