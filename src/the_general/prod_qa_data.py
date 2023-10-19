"""
Downloads an Last Day Report with data from all the client platforms, includes Productivity, QA and Adherence for The General.

"""
import utils.utils as utils
import utils.sharepoint_wrapper  as shwp
import pandas as pd
import utils.dbutils as dbutils
import numpy as np
import utils.dfutils as dfutils
import src.the_general.reports_configs as rconfig

# PRODUCTIVITY DATA COMING FROM TABLEAU
# AHT REPORT
# Getting Scripts Variables
EXPECTED_COLUMNS = rconfig.aht["expected_columns"]
DROP_COLUMNS = rconfig.aht["drop_columns"]
HEADERS = rconfig.aht["headers"]

# AVAIL REPORT
# Getting Scripts Variables
AVAIL_EXPECTED_COLUMNS = rconfig.avail["expected_columns"]
AVAIL_DROP_COLUMNS = rconfig.avail["drop_columns"]
AVAIL_HEADERS = rconfig.avail["headers"]

# QUALITY REPORT
# Getting Scripts Variables
QA_EXPECTED_COLUMNS = rconfig.qa["expected_columns"]
QA_DROP_COLUMNS = rconfig.qa["drop_columns"]
QA_HEADERS = rconfig.qa["headers"]

# ADHERENCE REPORT
# Getting Scripts Variables
ADH_EXPECTED_COLUMNS = rconfig.adh["expected_columns"]
ADH_DROP_COLUMNS = rconfig.adh["drop_columns"]
ADH_HEADERS = rconfig.adh["headers"]

# Getting Folder config details
print('Getting SharePoint context.')    
folder_key = "the_general_prod_qa"
sh_configs = utils.get_config('dshub_sharepoint_config')         # Config file
folder_id = sh_configs['folders'][folder_key]["id"]
SCHEMA = sh_configs['folders'][folder_key]["schema"]
TARGET_TABLE =  sh_configs['folders'][folder_key]["target_table"]
ctx = shwp.get_datascience_hub_ctx()  

def open_connection():
    conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
    cursor = conn.cursor()                                                                                   
    cursor.fast_executemany = True 
    return conn

def transformations(df, headers, drops, date_col = 'date'):    
    df.drop(columns=drops, inplace=True)
    df.columns = headers 
    df.dropna(subset=['agent_name'],inplace=True) 
    df[date_col] = df[date_col].astype('datetime64[ns]')  
    # df['tenure'] = np.where(df['tenure']=='NotFound', np.nan, df['tenure'])
    df = dfutils.fill_dataframe_nulls(df)

    return df

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """    
    print(f"Running script for {folder_key}: {folder_id}")       
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id=folder_id)     

    for file_id in file_ids:
        print("Accessing File with id: ", file_id)
        print('Downloading file')
        try:
            print('Opening database connection.') # Get Data Science Hub SharePoint context
            conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
            cursor = conn.cursor()                                                                                   
            cursor.fast_executemany = True   

            file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
            
            print('Loading AHT report into pandas DataFrame')
            df_aht = pd.read_excel(file_obj['contents'], sheet_name='Paste AHT Report')                                  # Read into a DataFrame 
            # Verify that expected columns match the actual dataframe columns
            df_aht = df_aht[EXPECTED_COLUMNS]
            # assert EXPECTED_COLUMNS in df_aht.columns.tolist(), 'Expected columns do not match actual dataframe columns' 
            
            print('Loading Avail report into pandas DataFrame')
            df_avail = pd.read_excel(file_obj['contents'], sheet_name='Paste Avail Report')                             # Read into a DataFrame 
            # Verify that expected columns match the actual dataframe columns
            df_avail = df_avail[AVAIL_EXPECTED_COLUMNS]
            # assert AVAIL_EXPECTED_COLUMNS == df_avail.columns.tolist(), 'Expected columns do not match actual dataframe columns'
                
            print('Loading Quality report into pandas DataFrame')
            df_qa = pd.read_excel(file_obj['contents'], sheet_name='Paste QA', usecols='B:K')                                       # Read into a DataFrame 
            # Verify that expected columns match the actual dataframe columns
            df_qa = df_qa[QA_EXPECTED_COLUMNS]
            # assert QA_EXPECTED_COLUMNS == df_qa.columns.tolist(), 'Expected columns do not match actual dataframe columns'

            print('Loading Adherence report into pandas DataFrame')
            df_adh = pd.read_excel(file_obj['contents'], sheet_name='Paste ADH Report')                                       # Read into a DataFrame 
            # Verify that expected columns match the actual dataframe columns
            df_adh = df_adh[ADH_EXPECTED_COLUMNS]
            # assert ADH_EXPECTED_COLUMNS == df_adh.columns.tolist(), 'Expected columns do not match actual dataframe columns'

            # Transform dataframe AHT
            print("Tranforming and uploading AHT report")
            df_aht = transformations(df_aht, HEADERS, DROP_COLUMNS)      
            conn = open_connection()                                        
            dbutils.perform_safe_delete_insert_with_keys(conn, ['date'], df_aht, SCHEMA, TARGET_TABLE)           

            # Transform dataframe AVAIL
            print("Tranforming and uploading Avail report") 
            df_avail['tenure']  =  pd.to_numeric( df_avail['tenure'], errors = 'coerce')
            df_avail = transformations(df_avail, AVAIL_HEADERS, AVAIL_DROP_COLUMNS)         
            conn = open_connection()                                        
            dbutils.perform_safe_delete_insert_with_keys(conn, ['date'], df_avail, SCHEMA, 'glb_avail')      
            
            # Transform dataframe AVAIL
            print("Tranforming and uploading quality report") 
            df_qa = transformations(df_qa, QA_HEADERS, QA_DROP_COLUMNS, 'evaluation_date')         
            conn = open_connection()                                        
            dbutils.perform_safe_delete_insert_with_keys(conn, ['evaluation_date'], df_qa, SCHEMA, 'glb_quality')    

            # Transform dataframe AHT
            print("Tranforming and uploading Adherence report")
            df_adh = transformations(df_adh, ADH_HEADERS, ADH_DROP_COLUMNS)      
            conn = open_connection()                                        
            dbutils.perform_safe_delete_insert_with_keys(conn, ['date'], df_adh, SCHEMA, 'glb_adherence')           
            
            print("Moving to Historical Folder")
            shwp.move_file_to_folder(ctx, sh_configs['folders'][folder_key]['historical_id'], file_id)
            print("Correctly moved to historical folder")
        except Exception as e:
            conn.rollback()
            print('Table not uploaded, rolling back to previous state \n Error Details: ', e)
         