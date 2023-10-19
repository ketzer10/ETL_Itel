# import packages
import utils.dfutils as dfutils
import pandas as pd
import numpy as np

def transforms_function_commits_accepts(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    sheets = [i for i in list(df.keys()) ]

    temp = pd.DataFrame({})
    for x in sheets:

        if "Sheet" in x or "SUMMARY" in x or "Combined" in x or "ERC" in x:
             continue

        sheet = df[x]
        
        sheet.columns = sheet.columns.astype(str)
        sheet = sheet.astype(str)
        index = sheet.index[sheet.iloc[:,2].str.contains('Accept')].to_list()[0]
        sheet = sheet.iloc[index+2:]
        sheet.columns = sheet.iloc[0]
        sheet = sheet.iloc[1:]

        sheet.columns.values[1] = "date"

        sheet["date"] = pd.to_datetime(sheet["date"], format="%Y-%m-%d", errors="coerce")

        sheet = sheet.dropna(subset=["date"])

        sheet = sheet.loc[:,~sheet.columns.str.contains('nan|Total|NaT')]

        sheet = pd.melt(sheet, id_vars="date", var_name='interval', value_name='committed_hours')

        sheet[["date","interval"]] = sheet[["date","interval"]].astype(str)
        sheet['half_hour_interval'] = sheet["date"]+" "+sheet["interval"]
        sheet['lob'] = str(x).upper().replace('-','').strip().replace(' ','_').replace('__','_')

        sheet = sheet.drop(["date","interval"], axis=1)

        sheet = dfutils.df_handling(sheet, info_transform_function["df_handling"])

        sheet["committed_hours"] = sheet["committed_hours"].fillna(0)
        sheet["committed_hours"] = sheet["committed_hours"]*0.5
        
        sheet = sheet.drop_duplicates()
        temp = pd.concat([temp,sheet])


    return temp