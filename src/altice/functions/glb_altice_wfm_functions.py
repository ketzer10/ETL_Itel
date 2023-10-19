# import packages
import utils.dfutils as dfutils
import pandas as pd
import numpy as np


def transforms_function_wfm_mbj_west(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    sheets = [i for i in list(df.keys())]
    print(sheets)
    temp = pd.DataFrame({})

    for x in sheets:

        sheet = df[x]
        count_tables = len([i for i in sheet.columns if "Unnamed" not in str(i)])
        
        for i in range(count_tables):

            temp2 = sheet.iloc[:,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]]
            temp2 = temp2.iloc[:,[0,1,5,6]]
            temp2['date'] = list(temp2.columns)[0]
            temp2.columns = ['interval','estimated_shrinkage_and_leakage','required_fte','scheduled_fte','date']
            temp2['department'] = x[9:].replace('-','').strip() if "-" in x else x
            temp = pd.concat([temp,temp2])

            sheet = sheet.drop(sheet.columns[[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]], axis = 1)

    
    df = dfutils.df_handling(temp, info_transform_function["df_handling"])
    df = df.dropna(subset=["interval"])

    df['forecast_o_u'] = df['scheduled_fte'] - df['required_fte']
    df['Scheduled_fte_less_shrink_and_leakage'] =  df['scheduled_fte']*(1-df['estimated_shrinkage_and_leakage'])
    df['forecast_o_u_w_shrink_and_leakage'] = df['Scheduled_fte_less_shrink_and_leakage'] - df['scheduled_fte']
    df['forecast_sl_w_shrink_and_leakage'] =  df['Scheduled_fte_less_shrink_and_leakage'] / df['scheduled_fte']
    df['forecast_hours'] = df['required_fte']/2

    df = df[['interval','estimated_shrinkage_and_leakage','required_fte','scheduled_fte','forecast_o_u','Scheduled_fte_less_shrink_and_leakage','forecast_o_u_w_shrink_and_leakage','forecast_sl_w_shrink_and_leakage','forecast_hours','date','department']]

    return df