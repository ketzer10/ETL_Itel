import utils.sharepoint_wrapper as shwp
import utils.dbutils as dbutils
import pandas as pd
import numpy as np
from utils.utils import get_config

def pipeline_default_folder(folder_key, transform_function ):

    sh_config = get_config("dshub_sharepoint_config")["folders"][folder_key]
    
    folder_id = sh_config["id"]
    sheet_name = sh_config["sheet_name"]
    delete_keys = sh_config["delete_keys"]
    folder_historical_id = sh_config['historical_id']
    schema = sh_config["schema"]
    target_table = sh_config["target_table"]

    print("Getting SharePoint context")
    ctx = shwp.get_datascience_hub_ctx()

    
    # Getting files IDs from the folder
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id = folder_id)
        
    for id in file_ids:
        print("Accessing File with id: ", id)
        print('Downloading file')
        try:  
            # Extraction Phase
            io_data = shwp.get_sharepoint_file_by_id(ctx, id)
            print(io_data['file_name'])
            print("Data succesfully downloaded \nReading into dataframe")
            df = pd.read_excel(io_data["contents"], sheet_name = sheet_name, dtype = 'str')
                
            # Transform
            try:
                df = transform_function(df)
            except Exception as e:
                raise Exception(f"Error While Execute Transform Function. {e}")
                
            # The DB does not interpret the NANs correctly, so we changed them to Nones       
            df = df.fillna(np.nan).replace([np.nan], [None])
                
            print(df)
                
            # Creating Database connection
            print("Opening connection to database")
            conn = dbutils.open_connection_with_scripting_account()
            cursor = conn.cursor() 
            cursor.fast_executemany = True
                
            print(schema, target_table)
            # Loading Phase
            try:
                print("Loading data into database")
                dbutils.perform_safe_delete_insert_with_keys(
                    conn = conn, 
                    delete_keys = delete_keys, 
                    source_df = df, 
                    schema = schema, 
                    target_table_name = target_table
                    )
            except Exception as e:
                    print(f"ERROR: {e}")   
            try:
                print("Moving to Historical Folder")
                # shwp.move_file_to_folder(ctx, folder_historical_id, id)
                print("Correctly moved to historical folder")
            except Exception as e:
                print(f"ERROR: {e}")           

        except Exception as e:
            print(e)