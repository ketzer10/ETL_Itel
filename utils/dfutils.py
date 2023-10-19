"""
Pandas dataframe utilities
"""

from calendar import c
import numpy as np
import pandas as pd
import re

def fill_dataframe_nulls(df: pd.DataFrame, *args):
    """Fills the dataframe with NULL like values with None. Default list to replace is [np.nan, 'NULL', 'nan'].
    It is possible to add more values to the list using the *args parameter passing the values after the required arguments

    Args:
        df (DataFrame): The dataframe to change the values from.

    Returns:
        [Dataframe]: The dataframe with the replaced values. 
    """

    null_list = [['null'], ['NULL'], ['nan'], ['NAN'], ['None'], [np.nan]]
    
    # Adds optional items to the null key
    for i in range(len(args)):
        null_list.append([args[i]])

    # Iterate through the null list and replace with np.nan
    for null_value in null_list:
        df.replace([null_value], [np.nan], inplace=True)

    # Fill NAs with np.nan because pandas could've inferred datatypes for certain columns and 
    # replaced the np.nans that were filled in the last step with np.NaT, etc. Then replace the 
    # np.nan with None 
    return_df = df.fillna(np.nan).replace([np.nan], [None])

    return return_df


##################################    DATA VALIDATION FUNCTIONS  ###############################################

def validate_date_columns(df: pd.DataFrame, columns: list, date_format = "%m/%d/%Y", raise_flag = False, errors = 'coerce'):
    '''
    Validate the date column from a dataframe, wrong values get deleted
    df= dataframe
    columns = list of columns name that need validation
    date_format = format date for to do validation
    '''
    try:
        for column in columns:
            df[column] = pd.to_datetime(df[column], exact = True, errors = errors, format = date_format)
            if raise_flag:
                index = df[df[column].isna()].index
                df.loc[index, 'flag'] = df.loc[index, 'flag'] + f'Wrong {column} format '
    except Exception as e:
        raise Exception(f"An error occurred while trying to validate and set the date column {e}")

    return df


def validate_text_columns(df: pd.DataFrame, columns: list):
    '''
    Validate the text column from a dataframe, the column element become a string
    df = dataframe
    columns = list of columns name that need validation
    '''
    try:
        for column in columns:
            df[column] = df[column].astype("str")
    except Exception as e:
        raise Exception(f"An error occurred while trying to validate and set the text column {e}")

    return df


def validate_datetime_columns(df: pd.DataFrame, columns: list, date_format = "%I:%M:%S %p", raise_flag = False, errors = 'coerce'):
    '''
    Validate the time columns from a dataframe, wrong values get deleted
    df = dataframe
    column = column name that need validation [LIST]
    date_format = format date for to do validation
    '''
    try:
        for column in columns:
            df[column] = pd.to_datetime(df[column], exact = True, errors = errors, format = date_format)
            if raise_flag:
                    index=df[df[column].isna()].index
                    df.loc[index, 'flag'] = df.loc[index, 'flag'] + f'Wrong {column} format '            
    except Exception as e:
        raise Exception(f"An error occurred while trying to validate and set the datetime column {e}")

    return df

def validate_boolean_columns(df: pd.DataFrame, columns: list):
    '''
    Validate the text column from a dataframe, the column element become a string
    df = dataframe
    columns = list of columns name that need validation
    '''
    try:
        for column in columns:
            df[column] = df[column].astype("bool" )
    except Exception as e:
        raise Exception(f"An error occurred while trying to validate and set the boolean column {e}")

    return df


def validate_duration_columns(df: pd.DataFrame, columns: list, hour_format = "%H:%M:%S", raise_flag = False, errors = 'coerce'):
    '''
    Validate the duration columns from a dataframe, wrong values get deleted
    df = dataframe
    column = column name that need validation [LIST]
    hour_format = format time duration for to do validation
    '''
    try:
        for column in columns:
            df[column] = pd.to_datetime(df[column], exact=False, errors = errors, format = hour_format)
            if raise_flag:
                    index=df[df[column].isna()].index
                    df.loc[index, 'flag'] = df.loc[index, 'flag'] + f'Wrong {column} format ' 
    except Exception as e:
        raise Exception(f"An error occurred while trying to validate duration column {e}")

    return df

def validate_convert_duration_columns_regex(df: pd.DataFrame, columns: list, regex = "(^\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)", raise_flag = False):
    '''
    Validate the duration columns from a dataframe, wrong values get deleted
    df = dataframe
    column = column name that need validation [LIST]
    regex = string for search match patterns and get hours, minutes and seconds
    '''
    try:
        for column in columns:
            df[column] = df[column].apply(lambda x: validate_and_convert_duration_time_to_sec(x, regex = regex))
            if raise_flag:
                    index=df[df[column].isna()].index
                    df.loc[index, 'flag'] = df.loc[index, 'flag'] + f'Wrong {column} format ' 
    except Exception as e:
        raise Exception(f"An error occurred while trying to validate duration column {e}")

    return df



def validate_int_columns(df: pd.DataFrame, columns: list, errors = 'coerce'):
    '''
    Validate the text column from a dataframe, the column element become a string
    df = dataframe
    columns = list of columns name that need validation
    '''
    try:
        for column in columns:

            df[column] = pd.to_numeric(df[column], errors = errors)
           
    except Exception as e:
        raise Exception(f"An error occurred while trying to validate and set the integer column {e}")

    return df


def validate_float_columns(df: pd.DataFrame, columns: list, errors = 'coerce'):
    '''
    Validate the text column from a dataframe, the column element become a string
    df = dataframe
    columns = list of columns name that need validation
    '''
    try:
        for column in columns:
            df[column] = pd.to_numeric(df[column], errors = errors)
            #df[column] = df[column].astype("float")
    except Exception as e:
        raise Exception(f"An error occurred while trying to validate and set the float column {e}")

    return df


##################################    CONVERSION    FUNCTIONS  ###############################################
def convert_duration_columns_to_sec(df: pd.DataFrame, columns: list):
    '''
    Validate the duration columns from a dataframe, calculate the time duration in second and become the type column to float 
    df = dataframe
    column = column name that need validation [LIST]
    '''
    try:
        for column in columns:
            df[column] = df[column].dt.hour*3600 + df[column].dt.minute*60 + df[column].dt.second
            df[column] = np.floor(df[column]).astype("Int64")
    except Exception as e:
        raise Exception(f"An error occurred while trying to convert the duration column to sec {e}")

    return df 


def strip_string_columns(df: pd.DataFrame, columns: list):
    """
    Removes leading and trailing spaces in the strings 
    """
    try:
        for column in columns:
            df[column] = df[column].str.strip()
    except Exception as e:
        raise Exception(f"Unable to strip string {e}")

    return df


def uppercase_string_columns(df: pd.DataFrame, columns: list):
    """
    Removes leading and trailing spaces in the strings 
    """
    try:
        for column in columns:            
            df[column] = df[column].str.upper()                 
    except Exception as e:
        raise Exception(f"Unable to uppercase string {e}")

    return df


def lowercase_string_columns(df: pd.DataFrame, columns: list):
    """
    Removes leading and trailing spaces in the strings 
    """
    try:
        for column in columns:
            df[column] = df[column].str.lower()      
    except Exception as e:
        raise Exception(f"Unable to lowercase string {e}")

    return df

def replace_values_in_columns(df: pd.DataFrame, replace_list: list, regex = False) -> pd.DataFrame:
    try:
        for replace in replace_list:
            for column in replace["columns"]:
                df[column] = df[column] = df[column].str.replace(replace["replace_this"], replace["for_this"], regex=regex )
    except Exception as e:
        raise Exception(f"An error occurred while trying to replace values in columns. {e}")
        
    return df


def convert_to_datetime_columns(df: pd.DataFrame, columns: list):
    '''
    Validate the time columns from a dataframe, wrong values get deleted
    df = dataframe
    column = column name that need validation [LIST]
    date_format = format date for to do validation
    '''
    try:
        for column in columns:
            df[column] = df[column].astype('datetime64[ns]')
    except Exception as e:
        raise Exception(f"An error occurred while trying to validate and set the datetime column {e}")

    return df


def validate_and_convert_duration_time_to_sec(x: str, regex: str = '(^\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)'):
    if type(x) != str:
        return np.nan
    res = re.findall(regex, x)
    if  len(res) == 0:
        return np.nan

    res = res[0]
    res_len = len(res)
    match res_len:
        case 3:
            hour = float(res[0])
            minute = float(res[1])
            second = float(res[2])
            return hour*3600 + minute*60 + second
        case 2:
            minute = float(res[0])
            second = float(res[1])
            return minute*60 + second
        case 1: 
            second = float(res[0])
            return second
        case _: 
            return np.nan

################################## CHANGES TO DF FUNCTIONS ###############################################
def change_dataframe_columns_name(df: pd.DataFrame, map_columns: dict) -> pd.DataFrame:
    """Changes a dataframe column names

    Args:
        df (pd.DataFrame): The dataframe to be operated on.
        map_columns (dict): A dictionary containing the column rename mappings. Eg. {"old_name": "new_name"}

    Raises:
        Exception: Raises exception when rename is not possible.

    Returns:
        [pd.DataFrame]: The Dataframe with the renamed columns
    """

    try:
        df.rename(columns = map_columns, inplace=True)
    except Exception as e:
        raise Exception(f"An error occurred while trying to change the column name {e}")

    return df 


def add_dataframe_column_with_value(df: pd.DataFrame, name_column: str, values = np.nan):
    df[name_column] = values
    return df


def add_dataframe_column_function(df: pd.DataFrame, name_column: str, function):
    df[name_column] = function
    return df


def stack_dfs(dfs: list, columns_dfs: list) -> pd.DataFrame:
    for df in dfs:
        if columns_dfs != df.columns.tolist():
            raise Exception(f"Expected column do not match actual dataframe columns {df.columns}")

    df = pd.concat(dfs, ignore_index=True)
    return df


def df_handling(df: pd.DataFrame, df_handling: dict) -> pd.DataFrame:
    for todo in df_handling.keys():
        match todo:
            case "validate_date_columns":
                print("Validating date columns")
                # default values parameters
                date_format = "%m/%d/%Y" 
                raise_flag = False
                if "parameters" in df_handling[todo].keys():
                    for key, value in df_handling[todo]["parameters"].items():
                        match key:
                            case "date_format":
                                date_format = value
                            case "raise_flag":
                                raise_flag = value
                df = validate_date_columns(df, df_handling[todo]["columns"], date_format = date_format, raise_flag = raise_flag) 
            case "validate_text_columns":
                print("Validating text columns")
                df = validate_text_columns(df, df_handling[todo])
            case "validate_int_columns":
                print("Validating int columns")
                df = validate_int_columns(df, df_handling[todo])
            case "validate_float_columns":
                print("Validating float columns")
                df = validate_float_columns(df, df_handling[todo])
            case "validate_datetime_columns":
                print("Validating datetime columns")
                # default values parameters
                date_format = "%I:%M:%S %p" 
                raise_flag = False
                if "parameters" in df_handling[todo].keys():
                    for key, value in df_handling[todo]["parameters"].items():
                        match key:
                            case "date_format":
                                date_format = value
                            case "raise_flag":
                                raise_flag = value
                df = validate_datetime_columns(df, df_handling[todo]["columns"], date_format = date_format, raise_flag = raise_flag)

            case "validate_duration_columns":
                print("Validating duration columns")
                # default values parameters
                raise_flag = False
                regex = "(^\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)"
                if "parameters" in df_handling[todo].keys():
                    for key, value in df_handling[todo]["parameters"].items():
                        match key:
                            case "hour_format":
                                hour_format = value
                            case "raise_flag":
                                raise_flag = value
                            case "regex":
                                regex = value
                
                df = validate_convert_duration_columns_regex(df, df_handling[todo]["columns"], regex = regex, raise_flag = raise_flag)
            case "rename_columns":
                print("Rename columns")
                df = change_dataframe_columns_name(df, df_handling[todo])
            case "order_columns":
                print("Order columns")
                df = df[df_handling[todo]]
            case "strip_string_columns":
                print("Stripping string")
                df = strip_string_columns(df, df_handling[todo])
            case "upper_string_columns":
                print("Changing string to uppercase")
                df = uppercase_string_columns(df, df_handling[todo])
            case "lower_string_columns":
                print("Changing string to lowercase")
                df = lowercase_string_columns(df, df_handling[todo])
            case "fill_df_nulls":
                print("Filling empty values with nulls")
                df = fill_dataframe_nulls(df, df_handling[todo])
            case "convert_to_datetime_columns":
                print("Convert datetime columns")
                df = convert_to_datetime_columns(df, df_handling[todo])                
            case "replace_values_in_columns":
                print("Replacing values in columns")
                df = replace_values_in_columns(df, df_handling[todo])

    return df
