import requests
import pandas as pd
import numpy as np
import datetime 


def request_file():
    # Download latest property
    with open("Private Property Price Index.xls", "wb") as f:
        f.write(requests.get("https://www.rvd.gov.hk/doc/en/statistics/his_data_4.xls").content)


def formulate_market_data():
    excel_file = pd.ExcelFile("./Private Property Price Index.xls")
    df = pd.read_excel(excel_file, sheet_name="Monthly  按月")

    df.drop(df.columns[[0, 2, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]], axis=1, inplace=True)
    df = df.loc[4:len(df) - 7]
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df.ffill(inplace=True)
    df = df.drop(index = [4, 5]).reset_index(drop=True)
    df.rename(columns = {'Unnamed: 1': 'Year', 'Unnamed: 5': 'Month', 'Unnamed: 8': 'A', 'Unnamed: 11': 'B','Unnamed: 14' : 'C', 'Unnamed: 17': 'D', 'Unnamed: 20' : 'E'}, inplace = True)
    df['Date'] = pd.to_datetime(df[['Year', 'Month']].assign(DAY = 1))
    df.drop(columns = ['Year', 'Month'], inplace = True)
    df = df.reindex(columns=['Date', 'A', 'B', 'C', 'D', 'E'])
    print(df.to_markdown())
    return df

#define a function that showcases a list of excel data
def formulate_housing_data():
    xlsx = pd.read_excel("./Raw Source.xlsx", sheet_name = None)
    list = []
    for num_tab in range(len(xlsx)):
       df = pd.read_excel("./Raw Source.xlsx",sheet_name = num_tab)
       df.drop(columns="Price(M)($)")
       df["Class"] = pd.cut(df['Area'], bins = [0,39.9,69.9,99.9,159.9,np.inf], labels = ['A','B','C','D','E'])
    #    print(df.to_markdown())
       list.append(df)
    return list

# Define a function that
def adjustment(row):
    date = row["PASP"]
    date_month = date.month
    date_year = date.year
    return date.month
    
    
# Price adjusted according to residential price index (price * price index / 100)  
def adjust(record):
     n_record = []
     
     for df in record:
         df["adjusted_price"] = df.apply(adjustment, axis = 1)
         n_record.append(df)
     return n_record
         
    
    
    
    
    
    
        
    
    

if __name__ == "__main__":
    #request_file()
    price_index_Df = formulate_market_data()
    record = formulate_housing_data()
    print(record)
    n_rec = adjust(record)
    print(n_rec)
    
    

