import pandas as pd
import numpy as np
import utils.dfutils as dfutils

def data_cleaner(df: pd.DataFrame, int_columns = [], float_columns = [], duration_columns = [], date_columns = []) -> pd.DataFrame:

    df.columns = df.columns.str.strip()
    # Int columns
    if len(int_columns) > 0:
        
        for column_name in int_columns:

            df[column_name] = df[column_name].replace([],'', regex=True)
            df[column_name] = np.floor(pd.to_numeric(df[column_name], errors='coerce')).astype('Int64')

        # df = dfutils.replace_values_in_columnsV2(df,int_columns,replace_list={
        #                 "replace_this": [''],
        #                 "for_this": ''
        #             }, regex=True)
                    
        # df = dfutils.validate_int_columns(df,int_columns)

    # Float columns
    if len(float_columns) > 0:

        for column_name in float_columns:

            df[column_name] = df[column_name].replace(['%'],'', regex=True)
            df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
        
        # df = dfutils.replace_values_in_columnsV2(df,float_columns,replace_list={
        #                 "replace_this": ['%'],
        #                 "for_this": ''
        #             }, regex=True)

        # df = dfutils.validate_float_columns(df,float_columns)

    # Duration Columns
    if len(duration_columns) > 0:
        
        # df = dfutils.replace_values_in_columnsV2(df,duration_columns,replace_list={
        #                     "replace_this": ['\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])'],
        #                     "for_this": ''
        #                 }, regex=True)
        # df = dfutils.replace_values_in_columnsV2(df,duration_columns,replace_list={
        #                     "replace_this": [';'],
        #                     "for_this": ':'
        #                 }, regex=True)    
         

        def convert(value):
                try:
                    value = str(value).split(':')
                    match len(value):
                            case 3:
                                hour = float(value[0])
                                minute = float(value[1])
                                second = float(value[2])
                                return hour*3600 + minute*60 + second
                            case 2:
                                minute = float(value[0])
                                second = float(value[1])
                                return minute*60 + second
                            case 1:
                                return float(value[0])
                except:
                    return np.nan               
        
        
        for column_name in duration_columns:

            df[column_name] = df[column_name].replace(['\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])'],'', regex=True)
            df[column_name] = df[column_name].apply(convert)
            df[column_name] = np.floor(pd.to_numeric(df[column_name], errors='coerce')).astype('Int64')
            df = df.rename(columns={column_name:column_name+"_sec"})
        
    # Date columns
    if len(date_columns) > 0:

        for column_name in date_columns: 

            df[column_name] = df[column_name].replace([''],'', regex=True)    
            df[column_name] = pd.to_datetime(df[column_name], format="%Y/%m/%d", errors='coerce')

    # Rename Columns
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace(' ','_')

    
    print(df.dtypes)
    
    return df
