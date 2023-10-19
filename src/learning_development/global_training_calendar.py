"""
Downloads Globa Trainig Calendar

"""
from asyncio import exceptions
import utils.utils as utils
import utils.sharepoint_wrapper as shwp
import pandas as pd
import utils.dbutils as dbutils
from src.learning_development.config.config_files import configs
from src.learning_development.functions import global_training_calendar_functions as functions
import utils.dfutils as dfutils


# Getting Configs
FOLDER_KEY = "global_training_calendar"
sh_config = utils.get_config("dshub_sharepoint_config")

# Getting Folder Config
FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
SCHEMA = sh_config["folders"][FOLDER_KEY]["schema"]
TARGET_TABLE = sh_config["folders"][FOLDER_KEY]["target_table"]
KEYS = ["account", "batch"]

print("Getting SharePoint context")
ctx = shwp.get_datascience_hub_ctx()

def main(optional: list):
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
            df = pd.read_excel(io_data["contents"], sheet_name = "Training Calendar", engine = "pyxlsb")
            df = df.dropna(subset = ["BATCH #", "ACCOUNT"]) 
            
            # data handling phase
            df = functions.transform_function_before(df)
            df = dfutils.df_handling(df, configs[FOLDER_KEY]["df_handling"])
            df = functions.transform_function_after(df)

            # Creating Database connection
            print("Opening connection to database")
            conn = dbutils.open_connection_with_scripting_account()
            cursor = conn.cursor() 
            cursor.fast_executemany = True
            
            # Loading Phase
            try:
                print("Loading data into database")
                dbutils.perform_safe_truncate_insert(df, conn, SCHEMA, TARGET_TABLE)
                print("Moving to Historical Folder")
                shwp.move_file_to_folder(ctx, sh_config['folders'][FOLDER_KEY]['historical_id'], id)
                print("Correctly moved to historical folder")
            except Exception as e:
                print(f"ERROR: {e}")           

        except Exception as e:
            print(e)