"""
Global Productivity Data for TDS - Fields Services 
 
CMD comand -> python .\run.py -i 45 -o 1

"""

from asyncio.windows_events import NULL
import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
from src.learning_development.config.config_files import configs 
import numpy as np


sh_config = utils.get_config("dshub_sharepoint_config")

print("Getting SharePoint context")
ctx = shwp.get_datascience_hub_ctx()

def main(optional: list):
   

    match optional[0]:
        case 1:
            # Getting Configs
            FOLDER_KEY = "glb_cx_daily_scores"

            # Getting Folder Config
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            FOLDER_HISTORICAL_ID = sh_config['folders'][FOLDER_KEY]['historical_id']
            SCHEMA = sh_config["folders"][FOLDER_KEY]["schema"]
            TARGET_TABLE = sh_config["folders"][FOLDER_KEY]["target_table"][0]
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
                    df = pd.read_excel(io_data["contents"], sheet_name = ["Raw Data 2023","Raw Data 2022","January 2021","February 2021","March 2021","April 2021","May 2021","June 2021 ","July 2021","August 2021","September 2021","October 2021","November 2021","December 2021"])
                    

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
                        dbutils.perform_safe_truncate_insert(
                        df,
                        conn,
                        SCHEMA,
                        TARGET_TABLE
                        )
                    except Exception as e:
                        print(f"ERROR: {e}")   
                    
                    """
                    try:
                        print("Moving to Historical Folder")
                        shwp.move_file_to_folder(ctx, FOLDER_HISTORICAL_ID, id)
                        print("Correctly moved to historical folder")
                    except Exception as e:
                        print(f"ERROR: {e}")           
                    """
                except Exception as e:
                    print(e)
        case 2:
            # Getting Configs
            FOLDER_KEY = "glb_cx_daily_scores"

            # Getting Folder Config
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            FOLDER_HISTORICAL_ID = sh_config['folders'][FOLDER_KEY]['historical_id']
            SCHEMA = sh_config["folders"][FOLDER_KEY]["schema"]
            TARGET_TABLE = sh_config["folders"][FOLDER_KEY]["target_table"][1]
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
                    df = pd.read_excel(io_data["contents"], sheet_name = ["Raw Data 2023","Raw Data 2022","January 2021","February 2021","March 2021","April 2021","May 2021","June 2021 ","July 2021","August 2021","September 2021","October 2021","November 2021","December 2021"])
                    

                    # data handling phase
                    df = configs["glb_cx_daily_reports_mtd"]["transform_function"](df, configs["glb_cx_daily_reports_mtd"]["info_transform_function"])
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
                        dbutils.perform_safe_truncate_insert(
                        df,
                        conn,
                        SCHEMA,
                        TARGET_TABLE
                        )
                    except Exception as e:
                        print(f"ERROR: {e}")   
                    
                    """
                    try:
                        print("Moving to Historical Folder")
                        shwp.move_file_to_folder(ctx, FOLDER_HISTORICAL_ID, id)
                        print("Correctly moved to historical folder")
                    except Exception as e:
                        print(f"ERROR: {e}")           
                    """
                except Exception as e:
                    print(e)           