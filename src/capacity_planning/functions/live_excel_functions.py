# import packages
import utils.dfutils as dfutils
import pandas as pd

def transforms_function_planned_training_template(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    return df

def transforms_function_consolidated_cap_plan_new_details(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    df = df.drop(columns=['unnamed:_0'])

    return df

def transforms_function_consolidated_cap_plan_hiring_details(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df = pd.melt(df, id_vars=["Category","Sites","BUs"], var_name="date",value_name="hiring")
    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    

    return df