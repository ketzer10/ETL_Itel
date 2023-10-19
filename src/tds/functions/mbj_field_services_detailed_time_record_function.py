# import packages
import utils.dfutils as dfutils
import pandas as pd
import numpy as np


def tds_detailed_time_record_function(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df = df.drop(['Unnamed: 0'], axis=1)
    df = df.loc[:,~df.columns.str.startswith('Unnamed')]
    df["Employee ID"] = df[df["Start"].str.contains("ID") == True]['Start']
    df[["Employee ID"]] = df[["Employee ID"]].ffill(axis=0)
    df["Employee ID"] = df["Employee ID"].apply(lambda x: str(x).split(" ")[1] if "ID" in str(x) else x)
    df = df[df["Activity"].str.contains(",|-|Totals") == False]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    return df