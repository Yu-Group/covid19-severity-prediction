import pandas as pd
from os.path import join as oj
import os

if __name__ == '__main__':
    import sys
    sys.path.append(oj(os.path.dirname(__file__), '../../raw/google_mobility/'))
    from load import load_google_mobility
else:
    from ...raw.google_mobility.load import load_google_mobility

def clean_google_mobility(data_dir='../../raw/google_mobility/', 
                          out_dir="."):
    ''' Clean Google Community Mobility Reports
    
    Parameters
    ----------
    data_dir : str; path to the data directory to find raw csv
    
    out_dir : str; path to the data directory to write cleaned csv
    
    Returns
    -------
    writes out cleaned csv file and returns clean data frame
    '''
   
    # Naming of region granularities
    rename_dict = {
        'sub_region_2': 'County',
        'sub_region_1': 'State/Province',
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
    goog_df = load_google_mobility(data_dir)
    
    # convert from wide to long format
    goog_df = pd.melt(goog_df, id_vars=rename_dict.keys(), value_vars=sector_dict.keys(), 
                      var_name='Sector', value_name='Percent Change')
    goog_df = goog_df.rename(columns=rename_dict)
    goog_df['Sector'] = goog_df['Sector'].apply(lambda x: sector_dict[x])

    for region_type in ['Country', 'State/Province', 'County']:
        this_granularity = goog_df[~goog_df[region_type].isna()].index
        goog_df.loc[this_granularity, 'Region Type'] = region_type
    
    # add countyFIPS for clean merge
    cur_dir = os.getcwd()
    os.chdir(data_dir)
    cnty_df = pd.read_csv("../../raw/county_ids/county_fips.csv").iloc[:-2,:]
    cnty_df = cnty_df.rename(columns = {"CountyName": "County", "StateName": "State/Province"})
    us_state_abbrev = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AS': 'American Samoa', 'AZ': 'Arizona', 'AR': 'Arkansas',
        'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia',
        'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 
        'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 
        'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 
        'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 
        'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 
        'MP': 'Northern Mariana Islands', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
        'PR': 'Puerto Rico', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee',
        'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VI': 'Virgin Islands', 'VA': 'Virginia', 'WA': 'Washington',
        'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
    }
    cnty_df["State/Province"] = cnty_df["State/Province"].replace(us_state_abbrev)
    os.chdir(cur_dir)
    
    # clean county names for clean merge
    cnty_df = clean_county_names(cnty_df, "county")
    goog_df = clean_county_names(goog_df, "google")
    
    # merge county fips
    goog_df = pd.merge(goog_df, cnty_df, on = ["County_cleaned", "State/Province"], how = "left")
    
    # clean columns
    goog_df = goog_df.rename(columns = {"County_x": "County"})
    goog_df.countyFIPS = goog_df.countyFIPS.str.zfill(5)
    goog_df = goog_df[["Region Type", "Country", "State/Province", "County", "countyFIPS",
                       "Date", "Sector", "Percent Change"]]
    
    goog_df.to_csv(oj(out_dir, 'google_mobility.csv'), index=False)
    return goog_df
    

def clean_county_names(df, df_name):
    
    df["County_cleaned"] = df.County
    
    if df_name == "google":
        df.County_cleaned = df.County_cleaned.replace({
            "Baltimore": "Baltimore Cty", "St. Louis": "St. Louis Cty", "Fairfax": "Fairfax Cty",
            "Franklin": "Franklin Cty", "Richmond": "Richmond Cty", "Roanoke": "Roanoke Cty", 
            "Doña Ana County": "Dona Ana", "Kenai Peninsula Borough": "Kenai Peninsula"
        })
    elif df_name == "county":
        df.County_cleaned = df.County_cleaned.replace({
            "Baltimore City": "Baltimore Cty", "St Louis City": "St Louis Cty", "Bedford City": "Bedford Cty", 
            "Fairfax City": "Fairfax Cty", "Franklin City": "Franklin Cty", "Richmond City": "Richmond Cty", 
            "Roanoke City": "Roanoke Cty"
        })
    
    df.County_cleaned = df.County_cleaned.str.lower()
    df.County_cleaned = df.County_cleaned.str.replace(".", "")
    df.County_cleaned = df.County_cleaned.str.replace("'", "")
    df.County_cleaned = df.County_cleaned.str.replace("county", "")
    df.County_cleaned = df.County_cleaned.str.replace("city", "")
    df.County_cleaned = df.County_cleaned.str.replace("parish", "")
    df.County_cleaned = df.County_cleaned.str.replace(" ", "")
    
    return df


if __name__ == '__main__':
    df = clean_google_mobility()
    print("cleaned google_mobility successfully.")