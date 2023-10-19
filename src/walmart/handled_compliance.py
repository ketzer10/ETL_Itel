"""
Downloads HANDLED COMPLIANCE

"""
from asyncio import exceptions
import utils.utils as utils
import utils.sharepoint_wrapper as shwp
import pandas as pd
import utils.dbutils as dbutils
from src.walmart.config.config_files import configs
from src.learning_development.functions import global_training_calendar_functions as functions
import utils.dfutils as dfutils


# Getting Configs
sh_config = utils.get_config("dshub_sharepoint_config")

print("Getting SharePoint context")
ctx = shwp.get_datascience_hub_ctx()

def main(optional: list):
    # Select correct folder
    match optional[0]:
        case 0: 
            folder_key = "handled_compliance_inbound"
        case 1: 
            folder_key = "handled_compliance_outbound"
        case 2:
            folder_key = "handled_compliance_outbound_jam"
        case 3:
            folder_key = "handled_compliance_inbound_jam"
        case 4:
            folder_key = "handled_compliance_outbound_geo"
        case 5:
            folder_key = "handled_compliance_inbound_geo"            

    FOLDER_ID = sh_config["folders"][folder_key]["id"]
    SCHEMA = sh_config["folders"][folder_key]["schema"]
    FLAG = sh_config["folders"][folder_key]["call_type_flag"]
    TARGET_TABLE = sh_config["folders"][folder_key]["target_table"]
    KEYS = configs[folder_key]["save_information"]["keys"]
    SITE = sh_config["folders"][folder_key]["site"]

    # Getting files IDs from the folder
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id = FOLDER_ID)
    
    for id in file_ids:
        print("Accessing File with id: ", id)
        print('Downloading file')
        try:  
            # Extraction Phase
            io_data = shwp.get_sharepoint_file_by_id(ctx, id)
            print(io_data['file_name'])
            print("Data succesfully downloaded")
            print("Reading into dataframe")
            df = pd.read_excel(io_data["contents"], sheet_name = "Export", )
            
            # Add date column in this case over Interval column
            # date = io_data['file_name'].split(".")[0]
            # date = date.split(" ")[1]
            # df["Interval"] = date
            # df["Interval"] = pd.to_datetime(df["Interval"], format = "%m-%d-%Y")

            # data handling phase
            # df = functions.transform_function_before(df)            
            df = dfutils.df_handling(df, configs[folder_key]["df_handling"])
            df["call_type"] = FLAG
            df["site"] = SITE
            #if SITE != "KGN":
                #df.dropna(subset=["forecast_adjustment"], inplace=True)
            #else:
                #df.dropna(subset=["handled"], inplace=True)

            df.dropna(subset=["handled"], inplace=True)
            # df = functions.transform_function_after(df)

            print(df)
            # Creating Database connection
            print("Opening connection to database")
            conn = dbutils.open_connection_with_scripting_account()
            cursor = conn.cursor() 
            cursor.fast_executemany = True
            
            # Loading Phase
            try:
                print("Loading data into database")
                dbutils.perform_safe_delete_insert_with_keys(conn, KEYS, df, SCHEMA, TARGET_TABLE)
                print("Moving to Historical Folder")
                shwp.move_file_to_folder(ctx, sh_config['folders'][folder_key]['historical_id'], id)
                print("Correctly moved to historical folder")
            except Exception as e:
                print(f"ERROR: {e}")           

        except Exception as e:
            print(e)