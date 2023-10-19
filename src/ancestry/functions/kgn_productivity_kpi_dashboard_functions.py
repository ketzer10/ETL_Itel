# import packages
import utils.dfutils as dfutils
import pandas as pd

def transform_function_qa(df: pd.DataFrame, info_transform_function: dict, **kwargs) -> pd.DataFrame:

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    df["average_score"] = df["average_score"]/100

    return df


def transform_function_csat(df: pd.DataFrame, info_transform_function: dict, **kwargs) -> pd.DataFrame:
    
    df["date"] = kwargs["file_name"].split("_")[-1].split(".")[0]
    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    for percent_column in ["percent_positive", "percent_negative", "percent_resolved"]:
        df[percent_column] = df[percent_column]/100

    return df