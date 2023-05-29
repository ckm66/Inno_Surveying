import pandas  as pd
import numpy as np

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

def time_index(trade_record, price_index_reference_table):
    PASP_Date = trade_record['PASP'].replace(day = 1)
    reference_row_no = price_index_reference_table.loc[price_index_reference_table['Date'] == PASP_Date].index[0]
    value = price_index_reference_table.loc[reference_row_no, trade_record["Class"]]
    return value


def unit_rate(trade_record, price_index_reference_table):
    PASP_Date = trade_record['PASP'].replace(day = 1)
    reference_row_no = price_index_reference_table.loc[price_index_reference_table['Date'] == PASP_Date].index[0]
    value = price_index_reference_table.loc[reference_row_no, trade_record["Class"]]
    return trade_record['Price($)'] *  (value / 100)

#define a function that showcases a list of excel data
def formulate_trade_record(price_index_reference_table):
    trade_record_list = []
    
    xlsx = pd.read_excel("./Raw Source.xlsx", sheet_name = None)
    for num_tab in range(len(xlsx)):
        df = pd.read_excel("./Raw Source.xlsx",sheet_name = num_tab)
            
        df.drop(columns="Price(M)($)", inplace = True)
        df["Class"] = pd.cut(df['Area'], bins = [0,39.9,69.9,99.9,159.9,np.inf], labels = ['A','B','C','D','E'])
        df["Time Index"] = df.apply(time_index ,args = (price_index_reference_table,),axis = 1)
        df["Unit Rate"] = df.apply(unit_rate ,args = (price_index_reference_table,),axis = 1)

        trade_record_list.append(df)
    return trade_record_list
