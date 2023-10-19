"""
Downloads Clients CSAT Report.

"""
import utils.utils as utils
import utils.dfutils as dfutils
import utils.sharepoint_wrapper  as shwp
import pandas as pd
import utils.dbutils as dbutils
import numpy as np
import src.kroger.reports_configs as rconfig
from datetime import datetime, timedelta

# Getting Scripts Variables
EXPECTED_COLUMNS = rconfig.quality["expected_columns"]
TA_EXPECTED_COLUMNS = rconfig.quality["team_expected_columns"]
HEADERS = rconfig.quality["headers"]
TA_HEADERS = rconfig.quality["team_headers"]
DROP_COLUMNS = rconfig.quality["drop_columns"]

# Getting Folder config details
print('Getting SharePoint context.')    
folder_key = "kroger_quality"
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
            # Creating Database connection.
            conn = dbutils.open_connection_with_scripting_account()                                                     # Constructing upsert statement.
            cursor = conn.cursor()                                                                                      # Creating database connection.
            cursor.fast_executemany = True   
            
            # Extraction io_data RAW DATA
            io_data = shwp.get_sharepoint_file_by_id(ctx, id)
            print("Data succesfully downloaded \nReading into dataframe")
            df = pd.read_excel(io_data['contents'], sheet_name='Raw Data')                                              # Reading files into pd.DataFrame
            # df = pd.read_excel("Kroger Daily CX Report-P5 (5).xlsx", sheet_name='Raw Data') 

            # Selecting only desired columns
            df = df[EXPECTED_COLUMNS]

            # Transforming dataframe
            df.drop(columns=DROP_COLUMNS, inplace=True)
            df.columns = HEADERS
            df['user_id'] = df['user_id'].str.strip().str.upper()
            df = df.fillna(np.nan).replace([np.nan], [None])                                                            # Filling NAs with Nones

            delete_date = df['evaluation_date'].max()-timedelta(days = 14)
            df = df[df['evaluation_date'] >= delete_date]
            
            dates = list(set(df['evaluation_date'].tolist()))
            dates = [ date.strftime("%Y-%m-%d") for date in dates]
            print('Dataframe read with ', df.shape)
            
            # == Uploading into database ==
            ## Deletting 14 days from the max date in the report and reuploading them from the new data

            del_stm = '''delete from {}.{} where evaluation_date in {}'''.format(SCHEMA, TARGET_TABLE, tuple(dates))
            cursor.execute(del_stm)
            print('Data Deleted for the last 25 dates in the report')
            param_slots = '('+', '.join(['?']*len(df.columns))+')'
            insert_statement = f"INSERT INTO {SCHEMA}.{TARGET_TABLE} VALUES {param_slots}"
            params = df.values.tolist()
            cursor.executemany(insert_statement, params)
            print(f'Importing to {SCHEMA}.{TARGET_TABLE}')
            conn.commit()

            print("New Data Commited")


            # Extraction TEAM ALIGNMENTS
            print('Reading Team Alignments')
            df = pd.read_excel(io_data['contents'], sheet_name='Agent Tenure', usecols='B:H')

            # Selecting Only desired Columns
            df = df[TA_EXPECTED_COLUMNS]

            # Transforming dataframe
            df.columns = TA_HEADERS
            df['user_id'] = df['user_id'].str.strip().str.upper()
            df = dfutils.fill_dataframe_nulls(df, 'None','N/A' )   
            df['hire_date'] = df['hire_date'].astype('datetime64[ns]')
            df.dropna(subset=['user_id', 'employee_name'], inplace=True)

            dbutils.perform_safe_truncate_insert(source_df = df, conn = conn, schema = SCHEMA, target_table_name='team_alignments')

            
            # Moving to Historical Folder
            print("Moving to Historical Folder")
            shwp.move_file_to_folder(ctx, sh_configs['folders'][folder_key]['historical_id'], id)
            print("Correctly moved to historical folder")
            

        except Exception as e:
            print("Error Downloading data \n Details: ",e)
        pass