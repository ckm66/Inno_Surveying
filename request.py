import requests
import pandas as pd
import numpy as np
import datetime 


def request_file():
    # Download latest property
    with open("Private Property Price Index.xls", "wb") as f:
        f.write(requests.get("https://www.rvd.gov.hk/doc/en/statistics/his_data_4.xls").content)


def formulate_price_index():
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
    return df

#define a function that showcases a list of excel data
def formulate_trade_record():
    xlsx = pd.read_excel("./Raw Source.xlsx", sheet_name = None)
    list = []
    for num_tab in range(len(xlsx)):
       df = pd.read_excel("./Raw Source.xlsx",sheet_name = num_tab)
       df.drop(columns="Price(M)($)", inplace = True)
       df["Class"] = pd.cut(df['Area'], bins = [0,39.9,69.9,99.9,159.9,np.inf], labels = ['A','B','C','D','E'])
       list.append(df)
    return list

  
def adjustment(trade_record, price_index_df):
    reference_row_no = price_index_df.loc[price_index_df['Date'].year == trade_record["PASP"].year & price_index_df['Date'].month == trade_record["PASP"].month].index[0]
    value = price_index_df.loc[reference_row_no, trade_record["Class"]]
    return trade_record["Price($)"] * value / 100
    
    
# Price adjusted according to residential price index (price * price index / 100)  
def adjust_time(trade_record_list, price_index_df):
    time_adjusted_record_list  = []
    for df in trade_record_list:
        df["Adjusted Price"] = df.apply(adjustment ,args = (price_index_df,),axis = 1)
        time_adjusted_record_list.append(df)
    return time_adjusted_record_list
             
if __name__ == "__main__":
    #request_file()
    price_index_df = formulate_price_index()
    trade_record_list = formulate_trade_record()
    trade_record_list = adjust_time(trade_record_list, price_index_df)
    
    

