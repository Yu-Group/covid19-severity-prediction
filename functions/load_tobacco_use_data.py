import pandas as pd

def loadTobaccoData():
    states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 
              'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 
              'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 
              'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 
              'Nebraska', 'Nevada', 'New%20Hampshire', 'New%20Jersey', 'New%20Mexico', 
              'New%20York', 'North%20Carolina', 'North%20Dakota', 'Ohio', 'Oklahoma', 'Oregon', 
              'Pennsylvania', 'Rhode%20Island', 'South%20Carolina', 'South%20Dakota', 
              'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 
              'West%20Virginia', 'Wisconsin', 'Wyoming', 'District%20of%20Columbia']
    data_ls = []
    for state in states:
        filepath = "./data/tobacco/smoking_data_" + state + ".xlsx"
        orig_data = pd.read_excel(filepath,
                                  sheet_name = "Ranked Measure Data", 
                                  skiprows = 1)
        data = orig_data[["FIPS", "% Smokers"]]
        #print(data.shape)
        data_ls.append(data)
    
    data = pd.concat(data_ls)
    data.columns = ["countyFIPS", "Smokers_Percentage"]
    return data