"""
Downloads an Client Reports with productivity data for Hilton KGN, MBJ and SLU. All the sites comes 
in the same report.
"""
import utils.utils as utils
import utils.sharepoint_wrapper  as shwp
import pandas as pd
import utils.dbutils as dbutils
import numpy as np
import src.hilton.reports_configs as rconfig

# Constant variables
# Getting Scripts Variables
EXPECTED_COLUMNS = rconfig.hilton_productivity["expected_columns"]
DROP_COULUMNS = rconfig.hilton_productivity["drop_columns"]
HEADERS = rconfig.hilton_productivity["headers"]
KEYS = rconfig.hilton_productivity["keys"]   

# Getting Folder config details
print('Getting SharePoint context.')    
folder_key = "hilton_prod"
sh_configs = utils.get_config('dshub_sharepoint_config')                                                                # Config file
folder_id = sh_configs['folders'][folder_key]["id"]
SCHEMA = sh_configs['folders'][folder_key]["schema"]
TARGET_TABLE = sh_configs['folders'][folder_key]["target_table"]
ctx = shwp.get_datascience_hub_ctx()                                                                                    # Sharepoint Client


def main(optional: list):
    
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id=folder_id)                                                    # Extracting files ids
    
    for id in file_ids:
        print("Accessing File with id: ", id)
        print('Downloading file')
        try: 
            # Extraction io_data 
            io_data = shwp.get_sharepoint_file_by_id(ctx, id)
            print(io_data["file_name"])
            print("Data succesfully downloaded \nReading into dataframe")
            # df = pd.read_excel(io_data['contents']) 
            # df = pd.read_excel("4.30.22_HRCC Agent Report - Partner.xlsx") 
            
            df = pd.read_excel(io_data['contents'], header = 2)              # Reading files into pd.DataFrame
            # df = pd.read_excel(io_data['contents'])              # Reading files into pd.DataFrame

            print("Reading file passed")
            # Selecting Only desired Columns
            df = df[EXPECTED_COLUMNS]
            print("Expected columns passed")
            # Transforming dataframe
            df.drop(columns=DROP_COULUMNS, inplace=True)
            df.columns = HEADERS
            df['agent_idm'] = df['agent_idm'].str.upper().str.strip()
            df = df.fillna(np.nan).replace([np.nan], [None])                                                            # Filling NAs with Nones
            
            print(df)
            # Creating Database connection.
            conn = dbutils.open_connection_with_scripting_account()                                                             # Constructing upsert statement.
            cursor = conn.cursor()                                                                                              # Creating database connection.
            cursor.fast_executemany = True   

            # == Uploading into database ==
            stm = dbutils.generate_dataframe_upsert_stmt(keys=KEYS, source_df=df, 
                                                        target_table_name=SCHEMA+'.'+TARGET_TABLE)
            print(f'Importing to {SCHEMA}.{TARGET_TABLE}')
            cursor.executemany(stm['stmt'], stm['params'])
            cursor.commit()
            print("New Data Commited")
            
            # Moving to Historical Folder
            print("Moving to Historical Folder")
            shwp.move_file_to_folder(ctx, sh_configs['folders'][folder_key]['historical_id'], id)
            print("Correctly moved to historical folder")

        except Exception as e:
            print("Error Downloading data \n Details: ",e)
        pass