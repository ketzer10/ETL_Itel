""" 
Downloads an Excel file containing productivity data from the SharePoint, uploads to the database and moves to archived.
"""

from multiprocessing.sharedctypes import Value
#from click import option
import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
import src.hrplus_sftp.transform_functions as transform_functions
from src.hrplus_sftp.configs import configs as script_configs



def sheet_downloader_and_uploader(case_name: str, file_type:str, mode:str , delete_keys:list = None):
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

    case_config = script_configs[case_name]
    config = utils.get_config("dshub_sharepoint_config")["folders"][case_config["sharepoint_config_key"]]
    folder_id = config["id"]
    folder_name = config["name"]
    historical_folder_id = config["historical_id"]
    schema = config["schema"]
    table_name = config["target_table"]
    #expected_columns = case_config["expected_cols"]
    use_cols = case_config["use_cols"]
    transform = case_config["transform_fn"]
    read_with_dtype = case_config["read_with_dtype"]

    print(f"Running script for {folder_name}: {folder_id}")       
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id=folder_id)        

    for file_id in file_ids:
        print("Accessing File with id: ", file_id)
        print("Downloading file")
        try:
            print("Opening database connection.") # Get Data Science Hub SharePoint context
            conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database

            file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
            print("Loading Excel file into pandas DataFrame.")
            if file_type == 'csv':
                df = pd.read_csv(file_obj["contents"], usecols=use_cols, dtype=read_with_dtype) # Read into a DataFrame                  
            elif file_type == 'xlsx':
                df = pd.read_excel(file_obj["contents"])
            else:
                raise ValueError ('Invalid file type')
            # Verify that expected columns match the actual dataframe columns
            #assert expected_columns == df.columns.tolist(), "Expected columns do not match actual dataframe columns"

            df = case_config["transform_fn"](df, case_config)

            # Upload to database
            if mode == 'truncate':
                dbutils.perform_safe_truncate_insert(df, conn, schema, table_name)
            elif mode == 'delete_insert':
                dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, df, schema, table_name)
            else:
                raise ValueError ('Invalid mode of operation.')

            # Moving to Historical Folder
            print("Moving to Historical Folder")
            #shwp.move_file_to_folder(ctx, historical_folder_id, file_id)
            print("Correctly moved to historical folder")        

            #df.to_csv(r"C:\Users\David.Nolasco\Desktop\blobs\HRPlus Exports Test\archived_upload.csv")    

        except Exception as e:
            conn.rollback()
            print("Table not uploaded, rolling back to previous state \n Error Details: ", e)
        pass 


def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """
    
    match optional[0]:
        case 1:
            case_name = "employees"
            sheet_downloader_and_uploader(case_name, file_type = 'csv', mode = 'truncate')
        case 2:
            case_name = "time_sheet"
            sheet_downloader_and_uploader(case_name, file_type = 'csv', mode = 'delete_insert', delete_keys=['dayWorked'])
        case 3:
            case_name = "positions"
            sheet_downloader_and_uploader(case_name, file_type = 'csv', mode = 'truncate')                    