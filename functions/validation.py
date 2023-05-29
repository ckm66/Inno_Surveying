import pandas as pd

def trade_record_validation():
    xlsx = pd.read_excel("./Raw Source.xlsx", sheet_name = None)
    building_names_list = []
    views_list = []
    for num_tab in range(len(xlsx)):
        df = pd.read_excel("./Raw Source.xlsx",sheet_name = num_tab)
        if (len(df['Building Name'].unique()) != 1 and len(df['Address'].unique()) != 1):
            raise ValueError(f"Sheet {num_tab} has more than one building name or address")
        
        if df['Building Name'].unique()[0] in building_names_list:
            raise ValueError(f"Sheet {num_tab} has more than one building name or address")
        building_names_list.append(df['Building Name'].unique()[0].replace(u'\xa0', u'').strip())
        
        for view in df['View'].unique():
            view = view.replace(u'\xa0', u'').strip()
            if view in views_list:
                continue
            views_list.append(view)
    return building_names_list, views_list