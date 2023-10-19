""" 
Downloads an Excel file containing Stella Internal QA from the SharePoint, uploads to the database and moves to archived.
"""

from numpy import timedelta64
import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils

def transformations(df, expected_columns):    

    df.columns = df.columns.str.replace(" ", "_")
    df.columns = df.columns.str.lower()
    df.rename(columns = {"name":"agent_name_site", "taker_name":"taker_name_site", "email": "agent_email", 
                        "custom_taker_id":"qa_custom_id", "taker_email":"qa_email", "taker_custom_id":"qa_custom_id"}, inplace = True)

    df.dropna(axis=0, subset=['assignment_id'],  inplace=True)
    df["date"] = ""

    df[['agent_name', 'site']] = df['agent_name_site'].str.split('_', 1, expand=True)
    df[['qa_name', 'qa_site']] = df['taker_name_site'].str.split('_', 1, expand=True)
    df.drop(['agent_name_site', 'taker_name_site', 'qa_site'], axis= 1, inplace=True)    
    
    date_columns = ['time_started', 'time_completed']

    df = dfutils.validate_datetime_columns(df, date_columns, date_format="%Y-%m-%d %H:%M:%S %Z")
    df['date'] = pd.to_datetime(df['time_completed'], format="%Y-%m-%d %H:%M:%S").dt.strftime("%Y-%m-%d")    
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
            df = pd.read_csv(file_obj["contents"]) # Read into a DataFrame

            # Transform dataframe
            df = transformations(df, expected_columns) 

            # Verify that expected columns match the actual dataframe columns
            assert expected_columns == df.columns.tolist(), "Expected columns do not match actual dataframe columns"

            # Upload to database
            dbutils.perform_safe_delete_insert_with_keys(conn, ["date", "site"], df, schema, table_name)

            # Moving to Historical Folder
            print("Moving to Historical Folder")
            shwp.move_file_to_folder(ctx, historical_folder_id, file_id)
            print("Correctly moved to historical folder")            

        except Exception as e:
            #conn.rollback()
            print("Table not uploaded, rolling back to previous state \n Error Details: ", e)
        pass 


def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """    

    expected_columns = ["interaction_id", "channel", "time_started", "time_completed", "agent_name", "agent_email", "custom_id", 
                        "qa_name", "qa_email", "qa_custom_id", "assignment_name","assignment_id", "scorecard_name", 
                        "section_name", "question_text", "answer_text", "site", "date"]
     
    folder_key = "walmart_internal_qa_stella"
        
    sheet_downloader_and_uploader(expected_columns, folder_key)