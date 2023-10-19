""" 
Downloads an Excel file containing productivity data from the SharePoint, uploads to the database and moves to archived.
"""

from msilib import schema
import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils

def transformations(df):
    print("Performing dataframe transformations.")
    df = dfutils.change_dataframe_columns_name(df, {"state_hours": "state_seconds"})
    df = dfutils.validate_date_columns(df, ["date"])
    df = dfutils.validate_datetime_columns(df, ["start_datetime", "end_datetime"], date_format = "%-m/%-d/%Y %-H:%M")
    df = dfutils.validate_float_columns(df, ["state_seconds"])
    df["state_seconds"] = df["state_seconds"] * 3600.0
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

    print("Getting SharePoint context.")
    ctx = shwp.get_datascience_hub_ctx() 

    config = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]
    folder_id = config["id"]
    historical_folder_id = config["historical_id"]
    schema = config["schema"]
    table_name = config["target_table"]

    print(f"Running script for {folder_key}: {folder_id}")       
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id=folder_id)        

    for file_id in file_ids:
        print("Accessing File with id: ", file_id)
        print("Downloading file")
        try:
            print("Opening database connection.") # Get Data Science Hub SharePoint context
            conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database

            file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
            print("Loading Excel file into pandas DataFrame.")
            df = pd.read_excel(file_obj["contents"]) # Read into a DataFrame

            # Verify that expected columns match the actual dataframe columns
            assert expected_columns == df.columns.tolist(), "Expected columns do not match actual dataframe columns"

            # Transform dataframe
            df = transformations(df)

            # Upload to database
            dbutils.perform_safe_delete_insert_with_keys(conn, ["date"], df, schema, table_name)

            # Moving to Historical Folder
            print("Moving to Historical Folder")
            shwp.move_file_to_folder(ctx, historical_folder_id, file_id)
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
    
    expected_columns = ["date","agent_name","country","line_business","state_name_one","state_name_two",
                        "state_id","start_datetime","end_datetime","state_hours"]     
    folder_key = "anyone_home_state_transactional_detail"
    sheet_downloader_and_uploader(expected_columns, folder_key)