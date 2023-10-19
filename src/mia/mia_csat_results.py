import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
from src.mia.config.config_files import configs

# Getting Configs
FOLDER_KEY = "mia_csat_results"
sh_config = utils.get_config("dshub_sharepoint_config")

# Getting Folder Config
FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
FOLDER_HISTORICAL_ID = sh_config['folders'][FOLDER_KEY]['historical_id']
SCHEMA = sh_config["folders"][FOLDER_KEY]["schema"]
TARGET_TABLE = sh_config["folders"][FOLDER_KEY]["target_table"]
DELETE_KEYS = ['date','dnis','ani']

print("Getting SharePoint context")
ctx = shwp.get_datascience_hub_ctx()

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """
    # Getting files IDs from the folder
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id = FOLDER_ID)
    
    for id in file_ids:
        print("Accessing File with id: ", id)
        print('Downloading file')
        try:  
            # Extraction Phase
            io_data = shwp.get_sharepoint_file_by_id(ctx, id)
            print(io_data['file_name'])
            print("Data succesfully downloaded \nReading into dataframe")
            df = pd.read_csv(io_data["contents"])

            df = configs[FOLDER_KEY]["transform_function"](df, configs[FOLDER_KEY]["info_transform_function"])
            df = dfutils.fill_dataframe_nulls(df, "")
            
            print(df)

            # Creating Database connection
            print("Opening connection to database")
            conn = dbutils.open_connection_with_scripting_account()
            cursor = conn.cursor() 
            cursor.fast_executemany = True
            print(df)
            dbutils.perform_safe_delete_insert_with_keys(conn,DELETE_KEYS,df,SCHEMA,TARGET_TABLE)

            try:
                print("Moving to Historical Folder")
                shwp.move_file_to_folder(ctx, FOLDER_HISTORICAL_ID, id)
                print("Correctly moved to historical folder")
            except Exception as e:
                print(f"ERROR: {e}")       

        except Exception as e:
            print(e)
