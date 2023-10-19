""" 
Downloads an Excel file containing ACD data from the SharePoint, uploads to the database and moves to archived.
"""

import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
import datetime as dt
import src.tds.functions.glb_tds_agent_status_functions as transform_fns


def sheet_downloader_and_uploader(read_columns:list, expected_columns: list, key: str, key_type: str):
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

    match key_type:
        case "folder":
            folder_id = utils.get_config('dshub_sharepoint_config')['folders'][key]['id']
            historical_folder_id = utils.get_config('dshub_sharepoint_config')['folders'][key]['historical_id']
            schema = utils.get_config('dshub_sharepoint_config')['folders'][key]['schema']
            table_name = utils.get_config('dshub_sharepoint_config')['folders'][key]['target_table']

            print(f"Running script for {key}: {folder_id}")       
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
                    df = transform_fns.tds_agent_status_transformations(df, read_columns, expected_columns)            

                    # Verify that expected columns match the actual dataframe columns
                    assert expected_columns == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'

                    # Upload to database
                    dbutils.perform_safe_delete_insert_with_keys(conn, ['date'], df, schema, table_name)

                    # Moving to Historical Folder
                    print("Moving to Historical Folder")
                    shwp.move_file_to_folder(ctx, historical_folder_id, file_id)
                    print("Correctly moved to historical folder")            

                except Exception as e:
                    conn.rollback()
                    print('Table not uploaded, rolling back to previous state \n Error Details: ', e)
                pass 

        case "file":
            schema = utils.get_config('dshub_sharepoint_config')['files'][key]['schema']
            table_name = utils.get_config('dshub_sharepoint_config')['files'][key]['target_table']   
            file_id = utils.get_config('dshub_sharepoint_config')['files'][key]['id']              
            print('Opening database connection.') # Get Data Science Hub SharePoint context
            conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
            print('Getting file from SharePoint site.')    
            file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
            print('Loading Excel file into pandas DataFrame.')
     
            df = pd.read_excel(file_obj['contents']) # Read into a DataFrame

            df = transform_fns.tds_billable_codes_transformations(df, read_columns)   

            # Verify that expected columns match the actual dataframe columns
            assert expected_columns == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'


            print('Truncating database and reinserting.')
            # Truncate and insert into the database
            dbutils.perform_safe_truncate_insert(df, conn, schema, table_name)

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """    
    match optional[0]:
        case 0:
            expected_columns = ["aspect_id", "status_start", "status_end", "status_type_desc", 
                                "reason_desc", "status_duration_sec", "date"]
            read_columns = ["employee_id", "status_start", "status_end", "status_type_desc", 
                            "reason_desc", "status_duration"]
            key = "tds_agent_status"
            key_type = "folder"
            sheet_downloader_and_uploader(read_columns, expected_columns, key, key_type)
        case 1:
            read_columns = ["status_type_desc", "reason_desc", "billable", "comment"]
            expected_columns = read_columns            
            key = "tds_billable_codes"
            key_type = "file"
            sheet_downloader_and_uploader(read_columns, expected_columns, key, key_type)            