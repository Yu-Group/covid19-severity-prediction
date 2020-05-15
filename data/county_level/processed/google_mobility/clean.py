import pandas as pd
from pathlib import Path

def clean(data_path='../../raw/google_mobility/google.csv',
            convenience_cols=True):
    """
    Clean google mobility data

    Output will have columns:
    - Country
    - State (also province, or any region bigger than county)
    - County
    - Date (YYYY-MM-DD)
    - Region Type (one of {County, State, Country}, level of granularity)
    - Sector (one of {parks, retail_and_recreation, transit, workplaces,
        residential, grocery_and_pharmacy})
    """
    # Naming of region granularities
    rename_dict = {
        'sub_region_2': 'County',
        'sub_region_1': 'State',
        'country_region': 'Country',
        'date': 'Date',
    }
    sector_dict = {
        'retail_and_recreation': 'Retail-Recreation',
        'grocery_and_pharmacy': 'Grocery-Pharmacy',
        'parks': 'Parks',
        'transit_stations': 'Transit',
        'workplaces': 'Workplace',
        'residential': 'Residential'
    }
    sector_dict = {k + '_percent_change_from_baseline': sector_dict[k] for k in sector_dict}
    
    # Load raw data
    goog_df = pd.read_csv(Path(__file__).parent.absolute() / data_path)
    goog_df = pd.melt(goog_df, id_vars=rename_dict.keys(), value_vars=sector_dict.keys(), 
                                var_name='Sector', value_name='Percent Change')
    goog_df = goog_df.rename(columns=rename_dict)
    goog_df['Sector'] = goog_df['Sector'].apply(lambda x: sector_dict[x])

    for region_type in ['Country', 'State', 'County']:
        this_granularity = goog_df[~goog_df[region_type].isna()].index
        goog_df.loc[this_granularity, 'Region Type'] = region_type
    goog_df.to_csv('google.csv', index=False)

if __name__ == '__main__':
    clean()