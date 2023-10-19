"""
Global Productivity Data for TDS - Sale 
 
CMD comand -> python .\run.py -i 43

"""
from asyncio import exceptions
import utils.sharepoint_wrapper as shwp
import utils.dbutils as dbutils
import utils.dfutils as dfutils
import utils.utils as utils
import pandas as pd
from src.tds.config.config_files import configs


# Getting Configs
FOLDER_KEY = "global_tds_sales_productivity"
sh_config = utils.get_config("dshub_sharepoint_config")

# Getting Folder Config
FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
FOLDER_HISTORICAL_ID = sh_config['folders'][FOLDER_KEY]['historical_id']
SCHEMA = sh_config["folders"][FOLDER_KEY]["schema"]
TARGET_TABLE = sh_config["folders"][FOLDER_KEY]["target_table"]
DELETE_KEYS = configs[FOLDER_KEY]["delete_key"]

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
            df = pd.read_excel(io_data["contents"], sheet_name = "DATA PULL", dtype = configs[FOLDER_KEY]["read_with_dtype"])
            df = df.dropna(subset=['agent_id'])

            # data handling phase
            df = configs[FOLDER_KEY]["transform_function"](df, configs[FOLDER_KEY]["info_transform_function"])
            df = dfutils.fill_dataframe_nulls(df, "")
            
            print(df.head(20))
            
            # Creating Database connection
            print("Opening connection to database")
            conn = dbutils.open_connection_with_scripting_account()
            cursor = conn.cursor() 
            cursor.fast_executemany = True
            
            
            # Loading Phase
            try:
                print("Loading data into database")
                dbutils.perform_safe_delete_insert_with_keys(
                    conn = conn, 
                    delete_keys = DELETE_KEYS, 
                    source_df = df, 
                    schema = SCHEMA, 
                    target_table_name = TARGET_TABLE
                )
            except Exception as e:
                print(f"ERROR: {e}")   
            try:
                print("Moving to Historical Folder")
                shwp.move_file_to_folder(ctx, FOLDER_HISTORICAL_ID, id)
                print("Correctly moved to historical folder")
            except Exception as e:
                print(f"ERROR: {e}")           

        except Exception as e:
            print(e)