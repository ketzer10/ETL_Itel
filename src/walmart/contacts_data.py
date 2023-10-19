""" 
Downloads an Excel file containing productivity data from the SharePoint, uploads to the database and moves to archived.
"""

import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils

def transformations(df, expected_columns):    
    df.columns = expected_columns
    df.dropna(subset=['agent_id'],inplace=True)  
    df['date'] = df['date'].astype('datetime64[ns]')

    intervals = df['thirty_minute_interval_start'].str.split('-', 2 ,expand=True)
    df['agent_name'] = df['agent_name'].str.split(',').str[::-1].str.join(' ').str.strip()
    
    df['thirty_minute_interval_start'] = intervals[0]
    date_interval = df['date'].astype('str')+' '+df['thirty_minute_interval_start']+':00'    
    df['thirty_minute_interval_start'] = pd.to_datetime(date_interval, format = "%Y-%m-%d %H:%M:%S")

    df['agent_id']=df['agent_id'].astype('int64')

    df = dfutils.fill_dataframe_nulls(df)

    return df

def sheet_downloader_and_uploader(expected_columns: list, folder_key: str):
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
    schema = utils.get_config('dshub_sharepoint_config')['folders'][folder_key]['schema']
    table_name = utils.get_config('dshub_sharepoint_config')['folders'][folder_key]['target_table']

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
            df = pd.read_excel(file_obj['contents']) # Read into a DataFrame

            # Transform dataframe
            df = transformations(df, expected_columns)            

            # Verify that expected columns match the actual dataframe columns
            assert expected_columns == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'

            # Upload to database
            dbutils.perform_safe_delete_insert_with_keys(conn, ['thirty_minute_interval_start', 'team_name'], df, schema, table_name)

            # Moving to Historical Folder
            print("Moving to Historical Folder")
            shwp.move_file_to_folder(ctx, historical_folder_id, file_id)
            print("Correctly moved to historical folder")            

        except Exception as e:
            conn.rollback()
            print('Table not uploaded, rolling back to previous state \n Error Details: ', e)
        pass 


def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """    
    
    expected_columns = ["date","thirty_minute_interval_start","agent_name","agent_id","team_name",
                        "logins", "held", "inbound", "transferred", "outbound_handled", "refusals", 
                        "holds", "inbound_handled", "refused", "handled", "in_sla", "out_sla"]
     
    folder_key = "walmart_call_contact_data"
        
    sheet_downloader_and_uploader(expected_columns, folder_key)