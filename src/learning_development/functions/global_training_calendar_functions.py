from src.learning_development.config.config_files import configs
import utils.dfutils as dfutils
from pyxlsb import convert_date
import pandas as pd
import numpy as np


FOLDER_KEY = "global_training_calendar"

def transform_function_before(df: pd.DataFrame) -> pd.DataFrame:
    
    
    # handling int columns
    for column in configs[FOLDER_KEY]["info_transform_function_before"]["int_columns"]:
        df[column] = df[column].replace([" ", "-", "nan", "TBD", "0xf"], [np.nan, np.nan, np.nan, np.nan, np.nan])
        df[column] = df[column].fillna(0)

    # handling float columns
    for column in configs[FOLDER_KEY]["info_transform_function_before"]["float_columns"]:
        df[column] = df[column].replace(["%", "-", "0xf"], [np.nan, np.nan, np.nan])
        df[column] = df[column].fillna(0.00)

    return df

def transform_function_after(df: pd.DataFrame) -> pd.DataFrame:
    for column in configs[FOLDER_KEY]["info_transform_function_affter"]["date_columns"]:
        df[column] = df[column].replace([" ", "-", "nan", "TBD"], [np.nan, np.nan, np.nan, np.nan])
        df[column] = df[column].fillna(0)
        df[column] = df[column].astype("int")
        df[column] = df[column].replace([0], [" "])
        df[column] = df[column].apply(lambda date: convert_date(date))

    df = dfutils.fill_dataframe_nulls(df, "")
    return df