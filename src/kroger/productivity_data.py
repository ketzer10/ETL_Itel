"""
Downloads an Client Reports with productivity data for Kroger.

"""
import src.kroger.reports_configs as rconfig
import utils.sharepoint_wrapper  as shwp
import utils.dfutils as dfutils
import utils.dbutils as dbutils
import utils.utils as utils
import pandas as pd
import numpy as np


# Getting Configs
FOLDER_KEY = "kroger_prod"
DF_HANDLING = rconfig.kroger_productivity["df_handling"]
KEYS = rconfig.kroger_productivity["keys"]
sh_config = utils.get_config("dshub_sharepoint_config")

# Getting Folder Config
FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
SCHEMA = sh_config["folders"][FOLDER_KEY]["schema"]
TARGET_TABLE = sh_config["folders"][FOLDER_KEY]["target_table"]

print('Getting SharePoint context.') 
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
            df = pd.read_excel(io_data['contents'], sheet_name = "Summary")
            
            # data handling phase
            df = dfutils.df_handling(df, DF_HANDLING)
            df = df.fillna(np.nan).replace([np.nan], [None])  
            df[['agent_occupancy_with_acw_pct','agent_occupancy_without_acw_pct']] = df[['agent_occupancy_with_acw_pct','agent_occupancy_without_acw_pct']]/100

            # Creating Database connection
            print("Opening connection to database")
            conn = dbutils.open_connection_with_scripting_account()                                                       
            cursor = conn.cursor()                                                                                             
            cursor.fast_executemany = True

            # Loading Phase
            try:
                print("Loading data into database")
                dbutils.perform_safe_delete_insert_with_keys(conn, KEYS, df, SCHEMA, TARGET_TABLE)
                # Moving to Historical Folder
                print("Moving to Historical Folder")
                shwp.move_file_to_folder(ctx, sh_config['folders'][FOLDER_KEY]['historical_id'], id)
                print("Correctly moved to historical folder")
            except Exception as e:
                print(f"ERROR: {e}")           

        except Exception as e:
            print("Error Downloading data \n Details: ", e)
        pass