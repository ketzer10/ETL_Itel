""" 
Downloads an Excel file containing Alignments from the SharePoint, uploads to the database and moves to archived.
"""

import numpy as np
import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils

def transformations(df, expected_columns):    

    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.replace(".", "")
    df.columns = df.columns.str.replace("/", "_")
    df.columns = df.columns.str.lower()

    df.dropna(axis=0, subset=['emp_id'],  inplace=True)    
    
    date_columns = ["hire_date", "nstg_date", "prod_date", "transfer_date", "attri_date"] 
    
    for column in date_columns:
        df[column] = df[column].replace("-", np.nan, inplace=True)
        df[column] = df[column].replace(" ", np.nan, inplace=True)
        df[column] = df[column].replace("", np.nan, inplace=True)
        df[column] = df[column].replace("1/0/1900", np.nan, inplace=True)
        df[column] = df[column].replace("00:00:00", np.nan, inplace=True)
    
    df = dfutils.convert_to_datetime_columns(df, date_columns)    
    df = dfutils.fill_dataframe_nulls(df)

    df = df[expected_columns]

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

    print("Getting SharePoint context.")
    ctx = shwp.get_datascience_hub_ctx() 

    folder_id = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]["id"]
    historical_folder_id = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]["historical_id"]
    schema = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]["schema"]
    table_name = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]["target_table"]

    print(f"Running script for {folder_key}: {folder_id}")       
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id=folder_id)     

    for file_id in file_ids:
        print("Accessing File with id: ", file_id)
        print("Downloading file")
        try:
            print("Opening database connection.") # Get Data Science Hub SharePoint context
            conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
            cursor = conn.cursor()                                                                                   
            cursor.fast_executemany = True

            file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
            print("Loading Excel file into pandas DataFrame.")
            df = pd.read_excel(file_obj["contents"], sheet_name="HC Roster") # Read into a DataFrame

            # Transform dataframe
            df = transformations(df, expected_columns) 

            # Verify that expected columns match the actual dataframe columns
            assert expected_columns == df.columns.tolist(), "Expected columns do not match actual dataframe columns"

            
            # Upload to database
            dbutils.perform_safe_delete_insert_with_keys(conn, ["site"], df, schema, table_name)

            # Moving to Historical Folder
            print("Moving to Historical Folder")
            #shwp.move_file_to_folder(ctx, historical_folder_id, file_id)
            print("Correctly moved to historical folder")            

        except Exception as e:
            conn.rollback()
            print("Table not uploaded, rolling back to previous state \n Error Details: ", e)
        pass 


def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """    

    expected_columns = ["bpo_wah", "site", "account", "emp_id", "status", "position", "full_name", 
                        "supervisor", "manager", "lob", "connection_type", "language", "vccid", "wm_login", 
                        "work_email", "wave", "hire_date", "nstg_date", "prod_date", "transferred_to", 
                        "transferred_from", "transfer_date", "attri_date", "attrition_type", "attrition_reason"]
     
    folder_key = "walmart_roster"
        
    sheet_downloader_and_uploader(expected_columns, folder_key)