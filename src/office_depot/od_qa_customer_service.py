""" 
Downloads an Excel file containing productivity data from the SharePoint, uploads to the database and moves to archived.
"""

from pickle import FALSE
from unittest import skip

from numpy import number
import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
from src.office_depot.config.report_manager_config import configs
pd.options.mode.chained_assignment = None  


def sheet_downloader_and_uploader(folder_key: str, delete_insert_keys: list, file_ext: str, read_with_dtype: str, qa_lob:str, skiprows = 0):
    """
    Reads all productivity Excel files in the folder and deletes and uploads to the database. 
    Args:        
        table_name (str): The name of the table to upload to. 
        output_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        folder_key (str): Name of the key of the folder in sharepoint.
    """

    print("Getting SharePoint context.")
    ctx = shwp.get_datascience_hub_ctx() 

    folder_id = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]["id"]
    historical_folder_id = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]["historical_id"]
    schema = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]["schema"]
    table_name = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]["target_table"]

    folders = shwp.get_folders_by_folder_id(ctx, folder_id)

    folder_dict = dict(zip(folders["folder_name"], folders["folder_id"]))

    for inner_folder_name, inner_folder_id in folder_dict.items():
        print(inner_folder_name, inner_folder_id)

        print(f"Running script for {folder_key}: {inner_folder_name}")       
        file_ids = shwp.get_files_by_folder_id(ctx, folder_id=inner_folder_id)     

        for file_id in file_ids:
            print("Accessing File with id: ", inner_folder_id)
            print("Downloading file")
            try:
                print("Opening database connection.")
                conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
                cursor = conn.cursor()                                                                                   
                cursor.fast_executemany = True            
                io_data = shwp.get_sharepoint_file_by_id(ctx, file_id)
                print(io_data['file_name'])
                print("Data successfully downloaded \nReading into dataframe")
                
                match file_ext:
                    case "csv":
                        df = pd.read_csv(io_data['contents'], skiprows=skiprows, dtype=read_with_dtype, on_bad_lines = 'skip')
                    case "xlsx":
                        df = pd.read_excel(io_data['contents'], skiprows=skiprows, dtype = read_with_dtype)

                # Transform dataframe
                df = configs[folder_key]["transform_function"](df, configs[folder_key]["info_transform_function"], lob = inner_folder_name)
                
                # Upload to database
                dbutils.perform_safe_delete_insert_with_keys(conn, delete_insert_keys, df, schema, table_name)

                # Moving to Historical Folder
                print("Moving to Historical Folder")
                shwp.move_file_to_folder(ctx, historical_folder_id, file_id)
                print("Correctly moved to historical folder")            

            except Exception as e:
                conn.rollback()
                print("Table not uploaded, rolling back to previous state \n Error Details: ", repr(e))
            pass 


def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """    
    qa_lob = ''
    match optional[0]:
        case 1:
            folder_key = "od_customer_service"
            file_ext = "csv"
            skiprows = 0

    read_with_dtype = configs[folder_key]["read_with_dtype"]
    delete_insert_keys = configs[folder_key]["delete_insert_keys"]
    sheet_downloader_and_uploader(folder_key=folder_key, 
                                  delete_insert_keys=delete_insert_keys, 
                                  file_ext=file_ext, 
                                  skiprows=skiprows, 
                                  read_with_dtype=read_with_dtype, 
                                  qa_lob=qa_lob)