import requests
import pandas as pd
import numpy as np


def request_file():
    # Download latest property
    with open("Private Property Price Index.xls", "wb") as f:
        f.write(requests.get("https://www.rvd.gov.hk/doc/en/statistics/his_data_4.xls").content)


def formuate_data():
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


if __name__ == "__main__":
    # requestFile()
    df = formuate_data()
