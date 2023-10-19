import utils.dfutils as dfutils
import pandas as pd
import numpy as np

def transforms_function_tds_hrm_employee_id(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    df = df.reindex(columns=['hrm_id','hrm_name','tds_name','tds_id','site','department'])

    return df