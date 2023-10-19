"""
Downloads an Last Day Report with data from all the client platforms, includes Productivity, QA and Adherence for The General.

"""
import utils.utils as utils
import utils.sharepoint_wrapper  as shwp
import pandas as pd
import utils.dbutils as dbutils
import numpy as np
import utils.dfutils as dfutils
import datetime
import src.the_general.reports_configs as rconfig
pd.options.mode.chained_assignment = None  # default='warn'

# Getting Scripts Variables
EXPECTED_COLUMNS = rconfig.sales["expected_columns"]
DROP_COLUMNS = rconfig.sales["drop_columns"]
HEADERS = rconfig.sales["headers"]
KEYS = rconfig.sales["keys"]

# Getting Folder config details
print('Getting SharePoint context.')    
folder_key = "the_general_sales_data"
sh_configs = utils.get_config('dshub_sharepoint_config')                                                                # Config file
folder_id = sh_configs['folders'][folder_key]["id"]
SCHEMA = sh_configs['folders'][folder_key]["schema"]
TARGET_TABLE = sh_configs['folders'][folder_key]["target_table"]
ctx = shwp.get_datascience_hub_ctx()  


def transformations(df, headers, drops, date_col = 'date'):   
    year = df.iloc[0,3]
    month = df.iloc[2,3]
    month = datetime.datetime.strptime(month, "%B")
    month_starting = datetime.date(year,month.month, 1)

    df.columns = headers
    df = df[4:]

    # df.drop(columns=drops, inplace=True)
    df.columns = headers 
    df.dropna(subset=['agent_name'],inplace=True) 

    df['quote_to_call'] = df['quotes']/df['calls']
    df['sales_to_call'] = df['sales']/df['calls']
    df['average_premium'] = df['sales_permium']/df['sales']
    df['close_rate'] = df['sales']/df['quotes']
    df['month'] = month_starting
    df = dfutils.fill_dataframe_nulls(df)

    return df 

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """    
    print(f"Running script for {folder_key}: {folder_id}")       
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id=folder_id)     
    conn = dbutils.open_connection_with_scripting_account()                                                              # Perform a connection to the database
    cursor = conn.cursor()     

    cursor.fast_executemany = True 
    for file_id in file_ids:
        print("Accessing File with id: ", file_id)
        print('Downloading file')
        try:
            print('Opening database connection.')                                                                       # Get Data Science Hub SharePoint context
            conn = dbutils.open_connection_with_scripting_account()                                                     # Perform a connection to the database
            cursor = conn.cursor()                                                                                   
            cursor.fast_executemany = True   

            file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id)                                                     # Get the file from the SharePoint
            print('Loading report into pandas DataFrame')
            df = pd.read_excel(file_obj['contents'], usecols='A:G',sheet_name='April')                                                     # Read into a DataFrame 

            # Transform dataframe AHT
            print("Tranforming and uploading report")
            df = transformations(df, HEADERS, DROP_COLUMNS)      
                                                  
            dbutils.perform_safe_delete_insert_with_keys(conn, KEYS, df, SCHEMA, TARGET_TABLE)           
            
            print("Moving to Historical Folder")
            # shwp.move_file_to_folder(ctx, sh_configs['folders'][folder_key]['historical_id'], file_id)
            print("Correctly moved to historical folder")
        except Exception as e:
            conn.rollback()
            print('Table not uploaded, rolling back to previous state \n Error Details: ', e)
        pass    