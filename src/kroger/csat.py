"""
Downloads Clients CSAT Report. The days argument provides the number of days that are going to be updated in the 
database, default value is 25 days.

"""
from sqlite3 import adapt
import utils.utils as utils
import utils.sharepoint_wrapper  as shwp
import pandas as pd
import utils.dbutils as dbutils
import numpy as np
import src.kroger.reports_configs as rconfig
from datetime import timedelta
from pyxlsb import open_workbook as open_xlsb, convert_date

# Getting Scripts Variables
EXPECTED_COLUMNS = rconfig.csat["expected_columns"]
DROP_COLUMNS = rconfig.csat["drop_columns"]
HEADERS = rconfig.csat["headers"]

# Getting Folder config details
print('Getting SharePoint context.')    
folder_key = "kroger_csat"
sh_configs = utils.get_config('dshub_sharepoint_config')                                                                # Config file
folder_id = sh_configs['folders'][folder_key]["id"]
SCHEMA = sh_configs['folders'][folder_key]["schema"]
TARGET_TABLE = sh_configs['folders'][folder_key]["target_table"]
ctx = shwp.get_datascience_hub_ctx()                                                                                    # Sharepoint Client

def main(optional = 25):
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id=folder_id)                                                    # Extracting files ids
    for id in file_ids:
        # Creating Database connection.
        conn = dbutils.open_connection_with_scripting_account()                                                             # Constructing upsert statement.
        cursor = conn.cursor()                                                                                              # Creating database connection.
        cursor.fast_executemany = True   
        print("Accessing File with id: ", id)
        print('Downloading file')
        try: 
            # Extraction io_data 
            io_data = shwp.get_sharepoint_file_by_id(ctx, id)
            print("Data succesfully downloaded \nReading into dataframe")
            df = pd.read_excel(io_data['contents'])                                                  # Reading files into pd.DataFrame

            # Verify that expected columns match the actual dataframe columns
            assert EXPECTED_COLUMNS == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'  
            # Transforming dataframe
            df.drop(columns=DROP_COLUMNS, inplace=True)
            df.columns = HEADERS
            df = df.fillna(np.nan).replace([np.nan], [None])                                                            # Filling NAs with Nones

            delete_date = df['response_date'].max()-timedelta(days = optional[0])
            df = df[df['response_date'] >= delete_date]
            dates = list(set(df['response_date'].tolist()))
            dates = [ date.strftime("%Y-%m-%d") for date in dates]
            print('Dataframe read with ', df.shape)
            
            # == Uploading into database ==
            ## Deletting 25 days from the max date in the report and reuploading them from the new data

            del_stm = '''delete from {}.{} where response_date in {}'''.format(SCHEMA, TARGET_TABLE, tuple(dates))
            cursor.execute(del_stm)
            print(f'Data Deleted for the last {optional[0]} dates in the report')
            param_slots = '('+', '.join(['?']*len(df.columns))+')'
            insert_statement = f"INSERT INTO {SCHEMA}.{TARGET_TABLE} VALUES {param_slots}"
            params = df.values.tolist()
            cursor.executemany(insert_statement, params)
            print(f'Importing to {SCHEMA}.{TARGET_TABLE}')
            conn.commit()
            conn.close()
            print("New Data Commited")
            
            # Moving to Historical Folder
            print("Moving to Historical Folder")
            shwp.move_file_to_folder(ctx, sh_configs['folders'][folder_key]['historical_id'], id)
            print("Correctly moved to historical folder")

        except Exception as e:
            print("Error Downloading data \n Details: ",e)
        pass