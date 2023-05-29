import requests

def request_file():
    # Download latest property
    with open("Private Property Price Index.xls", "wb") as f:
        f.write(requests.get("https://www.rvd.gov.hk/doc/en/statistics/his_data_4.xls").content)
