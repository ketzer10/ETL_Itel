""" 
Downloads an Excel file containing Login-Logout from the SharePoint, uploads to the database and moves to archived.
"""

import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils

def transformations(df, expected_columns):
    df['login_date']=''
    df.columns = expected_columns
    df.dropna(subset=['ps_id'],inplace=True)  
    df['logout_date'] = df['logout_date'].astype('datetime64[ns]')
    df['login_date_time'] = df['login_date_time'].astype('datetime64[ns]')
    
    df['login_date']=df['login_date_time'].astype('datetime64[ns]').dt.strftime("%Y-%m-%d")
    df['login_date_time'] = pd.to_datetime(df['login_date_time'], errors='coerce', format ="%Y-%m-%d %H:%M:%S")      

    df['logout_date_time'] = df['logout_date_time'].astype('datetime64[ns]')
    df['logout_date_time'] = pd.to_datetime(df['logout_date_time'], errors='coerce', format ="%Y-%m-%d %H:%M:%S") 

    df['login_duration_sec'] = df['login_duration_sec'].astype('datetime64[ns]')
    df['login_duration_sec'] = df['login_duration_sec'].dt.second + df['login_duration_sec'].dt.minute * 60 + df['login_duration_sec'].dt.hour * 3600

    print(df.columns)

    df = dfutils.fill_dataframe_nulls(df)

    return df

def sheet_downloader_and_uploader(expected_columns: list, folder_key: str, schema: str, table_name: str):
    """
    Reads all productivity Excel files in the folder and deletes and uploads to the database. 
    Args:        
        table_name (str): The name of the table to upload to. 
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        folder_key (str): Name of the key of the folder in sharepoint.
    """
    print('Getting SharePoint context.')
    ctx = shwp.get_datascience_hub_ctx()
   

    folder_id = utils.get_config('dshub_sharepoint_config')['folders'][folder_key]['id']    
    historical_folder_id = utils.get_config('dshub_sharepoint_config')['folders'][folder_key]['historical_id']
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
            print('Loading Excel file into pandas DataFrame.')
            df = pd.read_csv(file_obj['contents'], dtype=object) # Read into a DataFrame

            # Transform dataframe
            df = transformations(df, expected_columns)    

            print(df)              

            # Verify that expected columns match the actual dataframe columns
            assert expected_columns == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'           
            
            dbutils.perform_safe_delete_insert_with_keys(conn, ['logout_date'], df, schema, table_name)

            # Moving to Historical Folder
            print("Moving to Historical Folder")
            shwp.move_file_to_folder(ctx, historical_folder_id, file_id)
            print("Correctly moved to historical folder")                       

        except Exception as e:
            #conn.rollback()
            print('Table not uploaded, rolling back to previous state \n Error Details: ', e)
        pass 

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """    
    schema = 'altice'
    expected_columns = ['login_name','first_name','last_name','ps_id','logout_date','login_date_time','logout_date_time',
                        'login_duration_sec','reason_code','login_date']

    folder_key = 'altice_login_logout'
    table_name = 'glb_login_logout'
    sheet_downloader_and_uploader(expected_columns, folder_key, schema, table_name)