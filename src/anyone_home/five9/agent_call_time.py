""" 
Downloads an Excel file containing Agent Call Data from the SharePoint, uploads to the database and moves to archived.
"""

from datetime import datetime
import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils

def duration_to_seconds(df, duration_columns: list):
    for column in duration_columns:
        df[column] = df[column].astype('datetime64[ns]')
        df[column] = df[column].dt.second + df[column].dt.minute * 60 + df[column].dt.hour * 3600
    return df

def transformations(df, expected_columns):   
    df.columns = expected_columns 
    df.dropna(subset=['agent_id', 'agent_group'],inplace=True)      

    df['agent_id']=df['agent_id'].astype('int64')
    df['date'] = df['date'].astype('datetime64[ns]')

    duration_columns = ['talk_sec', 'hold_sec', 'park_sec', 'acw_sec', 'handling_sec']
    df = duration_to_seconds(df, duration_columns)

    drop_us=df[(df.agent_group.isin(['US Agents','Support', 'EQR Team']))].index
    df.drop(labels=drop_us, axis=0, inplace=True)   

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

            # Verify that expected columns match the actual dataframe columns
            assert expected_columns == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'

            # Upload to database
            dbutils.perform_safe_delete_insert_with_keys(conn, ['date'], df, schema, table_name)

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
    
    expected_columns = ['date', 'agent_group', 'agent_id', 'email', 'calls', 'talk_sec', 'hold_sec', 'park_sec', 'acw_sec', 
                        'handling_sec', 'transfer_skill', 'transfer_agent', 'transfer_campaign', 'transfer_queue']
    folder_key = 'anyone_home_agent_call_data'
    schema = 'anyone_home'
    table_name = 'glb_agent_call_data'
        
    sheet_downloader_and_uploader(expected_columns, folder_key, schema, table_name)