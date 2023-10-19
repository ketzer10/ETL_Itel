import utils.dfutils as dfutils
import pandas as pd
import numpy as np


def transforms_function_bus_arrival_departure_log(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    return df

def transforms_function_vehicle_capacities(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    return df

def transforms_function_trip_costs(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    return df


def transforms_function_honduras_trip_cost(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 


    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    return df