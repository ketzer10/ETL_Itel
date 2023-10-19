# import packages
import utils.dfutils as dfutils
import pandas as pd
import numpy as np


def transforms_function_sales_productivity(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 
    # delete rows with all columns empty
    df = df.drop(["Unnamed: 0"], axis = 1)
    df = df.dropna(how = "all", axis = 0)
    df = df.reset_index(drop = True)

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    df["projection"] = df["projection"].round()

    return df

def transforms_function_repair_productivity(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 
    
    df['quality_score'] = df['quality_score'] / 100
    
    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    return df

def transforms_function_financial_services_productivity(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 
    
    df[['average_handle_out','average_handle_in']] = df[['average_handle_out','average_handle_in']].astype('str')
    df[['average_handle_out','average_handle_in']] = df[['average_handle_out','average_handle_in']].replace(':00','', regex=True)

    df['week_start'] = pd.to_datetime(df['week_start'], errors='coerce')
    df['week_end'] = pd.to_datetime(df['week_end'], errors='coerce')

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    cols_percent = ["adherence", "would_hire", "quality_audits", "dpa_audits", "processing_audits"]
    for col in cols_percent:
        index = df[df[col] > 1].index
        df.loc[index, col] = df.loc[index, col]/100

    return df

def transforms_function_fields_services_productivity(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame:

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    df = df.dropna(subset=['agent_id','agent_name','date']) 

    return df

