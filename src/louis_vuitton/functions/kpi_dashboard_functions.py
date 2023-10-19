# import packages
import utils.dfutils as dfutils
import pandas as pd

def transform_function_percent_on_queve(df: pd.DataFrame, info_transform_function: dict, **kwargs) -> pd.DataFrame:

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    df["login"] = df["login"].dt.time
    df["logout"] = df["logout"].dt.time

    return df


def transform_function_quality_assessment(df: pd.DataFrame, info_transform_function: dict, **kwargs) -> pd.DataFrame:

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    df["start_time"] = df["start_time"].dt.time
    df["completion_time"] = df["completion_time"].dt.time

    return df


def transform_function_service_level_requirement(df: pd.DataFrame, info_transform_function: dict, **kwargs) -> pd.DataFrame:

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    return df


def transform_function_client_report(df: pd.DataFrame, info_transform_function: dict, **kwargs) -> pd.DataFrame:

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    return df