from typing import List
import utils.dfutils as dfutils
import pandas as pd

def format_time_columns(df, time_columns, time_format):
    for column in time_columns:
        df[column] = df[column].dt.strftime(time_format)
    return df

def format_date_column(df, date_columns, date_format):
    for column in date_columns:
        df[column] = df[column].dt.strftime(date_format)
    return df

def altice_sched_handling(df: pd.DataFrame, expected_columns: list, rename_columns:dict, time_columns:list, date_columns:list, 
                          time_format:str, date_format:str, code_remap_start:list, code_remap_end:dict, index_columns:dict,
                          output_columns:list):
    """
    Formats and outputs a dataframe for scheduling
    Args:
        df (pd.DataFrame): Schedule dataframe
        expected_columns (list): Columns expected from the input file
        rename_columns (dict): Columns to rename:New name
        time_columns (list): Columns that require time format
        date_columns (list): Columns that require date format
        time_format (str): String in Standard C DateTime Format 
        date_format (str): String in Standard C DateTime Format 
        code_remap_start (dict): Dict to remap start codes
        code_remap_end (dict): Dict to remap start codes
        index_columns (list): Unique identifiers
        output_columns (list): Columns for output format
    """
    df = df[expected_columns]

    df = dfutils.change_dataframe_columns_name(df, rename_columns)
    print("Renamed columns.")

    df[time_columns] = df[time_columns].astype("string")
    df = dfutils.strip_string_columns(df, time_columns)

    df = dfutils.validate_datetime_columns(df, time_columns, date_format='%H:%M %p')
    print("Validated time.")
    df = dfutils.validate_date_columns(df = df, columns = date_columns)
    print("Validated date.")

    df = format_time_columns(df, time_columns)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns)
    print("Formatted date", date_format)

    start_code_row_filter = list(code_remap_start.keys())
    print("Codes for schedules:", start_code_row_filter)
    df =  df[df["Code"].isin(start_code_row_filter)]
    df_start = df.drop(columns = ["Stop"])
    df_end = df.drop(columns = ["Start"])

    for codes in code_remap_start.items():
        df_start = df_start.replace(codes[0], codes[1])    

    for codes in code_remap_end.items():
        df_end = df_end.replace(codes[0], codes[1])

    print("Pivoting on", index_columns)
    df_pivot_start = pd.pivot(df_start, index = index_columns, columns = "Code", values = "Start").reset_index()
    df_pivot_end = pd.pivot(df_end, index = index_columns, columns = "Code", values = "Stop").reset_index()
    df_pivot_merged = df_pivot_start.merge(right = df_pivot_end, how = "left", on = index_columns)
    print("Merged", df_pivot_start.columns.to_list(), "with", df_pivot_end.columns.to_list(), "on", index_columns)

    df_output = df_pivot_merged[output_columns]

    return(df_output)