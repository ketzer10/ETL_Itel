"""
Downloads team alignments for hilton coming from Ash and WFM, the purpose of the data is to alocate the agents in their
respective site since all the sites comes in the same report.
"""
import utils.utils as utils
import utils.sharepoint_wrapper  as shwp
import pandas as pd
import utils.dbutils as dbutils
import utils.dfutils as dfutils
import src.hilton.reports_configs as rconfig

# Constant variables
# Getting Scripts Variables
EXPECTED_COLUMNS = rconfig.team_alignments["expected_columns"]
HEADERS = rconfig.team_alignments["headers"]
TRIM_COLUMNS = rconfig.team_alignments["trim_columns"]
UPPER_COLUMNS = rconfig.team_alignments["upper_columns"]
PROPER_COLUMNS = rconfig.team_alignments["proper_columns"]

# Getting Folder config details
print('Getting SharePoint context.')    
folder_key = "hilton_team_alignments"
sh_configs = utils.get_config('dshub_sharepoint_config')                                                                # Config file
folder_id = sh_configs['folders'][folder_key]["id"]
SCHEMA = sh_configs['folders'][folder_key]["schema"]
TARGET_TABLE = sh_configs['folders'][folder_key]["target_table"]
ctx = shwp.get_datascience_hub_ctx()                                                                                    # Sharepoint Client


def main(optional: list):
    # Creating Database connection.
    conn = dbutils.open_connection_with_scripting_account()                                                             # Constructing upsert statement.
    cursor = conn.cursor()                                                                                              # Creating database connection.
    cursor.fast_executemany = True   
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id=folder_id)                                                    # Extracting files ids
    
    for id in file_ids:
        print("Accessing File with id: ", id)
        print('Downloading file')
        try: 
            # Extraction io_data 
            io_data = shwp.get_sharepoint_file_by_id(ctx, id)
            print("Data succesfully downloaded \nReading into dataframe")
            df = pd.read_excel(io_data['contents'])                                                                     # Reading files into pd.DataFrame

            # Verify that expected columns match the actual dataframe columns
            assert EXPECTED_COLUMNS == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'  

            # Transforming dataframe
            df.columns = HEADERS

            for column in TRIM_COLUMNS:
                df[column] = df[column].astype(str)
                df[column] = df[column].str.strip()
            for column in UPPER_COLUMNS:
                df[column] = df[column].str.upper()
            for column in PROPER_COLUMNS:
                df[column] = df[column].str.title()

            df = dfutils.fill_dataframe_nulls(df, 'N/A')                                                                # Filling NAs with Nones
            
            df['hire_date'] = pd.to_datetime(df['hire_date'], errors='coerce')
            df['term_date'] = pd.to_datetime(df['term_date'], errors='coerce')
            # == Uploading into database ==
            print(f'Importing to {SCHEMA}.{TARGET_TABLE}')
            dbutils.perform_safe_truncate_insert(df, conn=conn, schema=SCHEMA, target_table_name=TARGET_TABLE)
            print("New Data Commited")
            
            # Moving to Historical Folder
            print("Moving to Historical Folder")
            shwp.move_file_to_folder(ctx, sh_configs['folders'][folder_key]['historical_id'], id)
            print("Correctly moved to historical folder")

        except Exception as e:
            print("Error Downloading data \n Details: ",e)
        pass