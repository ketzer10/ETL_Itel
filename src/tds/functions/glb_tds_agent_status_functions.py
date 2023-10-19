from datetime import datetime
import utils.dfutils as dfutils
import pandas as pd
import numpy as np

def tds_agent_status_transformations(df, read_columns, expected_columns):
    df.columns = df.columns.str.lower()
    df = df[read_columns]
    df['date'] = pd.to_datetime(df['status_start']).dt.date

    date_column = ["date"]
    datetime_columns = ["status_start", "status_end"]

    df = dfutils.validate_date_columns(df, date_column, date_format="%Y-%m-%d")
    df = dfutils.validate_datetime_columns(df, datetime_columns, date_format = "%Y-%m-%d %H:%M:%S")

    print(df.head())
    df.columns = expected_columns
    df['aspect_id']=df['aspect_id'].astype('int64')    
    df = df[expected_columns]

    df = dfutils.fill_dataframe_nulls(df)

    return df

def tds_billable_codes_transformations(df, read_columns):
    df.columns = df.columns.str.lower()
    df = df[read_columns]
    print(df.head())

    df = dfutils.fill_dataframe_nulls(df)

    return df