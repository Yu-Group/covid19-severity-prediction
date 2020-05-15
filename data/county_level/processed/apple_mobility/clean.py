import pandas as pd 

def clean(data_path='../../raw/apple_mobility/apple.csv'):
    """
    Saves CSV with columns:
    - Date
    - Sector (walking, driving, or transit)
    - Region Type (country/region, sub-region, city)
    - Percent Change (difference in mobility from baseline)
    """
    GOOD_COLS = {
        "geo_type": "Region Type",
        "region": "Region",
        "transportation_type": "Sector"
    }
    df = pd.read_csv(data_path)
    del df['alternative_name'] 
    df = pd.melt(df, id_vars=GOOD_COLS.keys(),
                    value_vars=set(df.columns) - set(GOOD_COLS.keys()), 
                    var_name='Date', value_name='Percent Change')
    df['Percent Change'] = df['Percent Change'] - 100.
    df = df.rename(columns=GOOD_COLS)
    df.to_csv('apple.csv')
    
if __name__ == '__main__':
    clean()