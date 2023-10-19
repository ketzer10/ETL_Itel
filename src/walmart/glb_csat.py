"""
Downloads Clients CSAT Report.

"""

import utils.utils as utils
import utils.sharepoint_wrapper as shwp
import pandas as pd
import utils.dbutils as dbutils
import src.walmart.reports_configs as rconfig
from datetime import datetime
import utils.dfutils as dfutils
import numpy as np


# Getting Configs
FOLDER_KEY = "walmart_glb_csat"
sh_config = utils.get_config("dshub_sharepoint_config")

# Getting Folder Config
FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
SCHEMA = sh_config["folders"][FOLDER_KEY]["schema"]
TARGET_TABLE = sh_config["folders"][FOLDER_KEY]["target_table"]

# Getting Report Variable
SELECTED_COLUMNS = rconfig.glb_csat["selected_columns"]
DROP_COLUMNS = rconfig.glb_csat["drop_columns"]
PCT_COLUMNS = rconfig.glb_csat["pct_columns"]
HEADERS = rconfig.glb_csat["headers"]
KEYS = rconfig.glb_csat["keys"]

print("Getting SharePoint context")
ctx = shwp.get_datascience_hub_ctx()

def transfomation(df, HEADERS, PCT_COLUMNS, report_date):
    # df[['Name','site']] = df['Name'].str.split( '_',n=4, expand = True) # we add "[[0, 1]]" for work well
    df[['Name','site']] = df['Name'].str.split( '_', expand = True)[[0, 1]]
    df.columns = HEADERS
    df['date'] = report_date
    for column in PCT_COLUMNS:
        df[column] = df[column].fillna('').astype('str').str.strip('%')
        df[column] = pd.to_numeric(df[column])/100
        df[column] = df[column].apply(lambda x: round(x, 10))
    
    df = dfutils.fill_dataframe_nulls(df)
    df.dropna(subset = ['custom_employee_id','name'], inplace = True)
    return df


def main(optional: list):
    # Getting files IDs from the folder
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id=FOLDER_ID)

    for id in file_ids:
        # Creating Database connection
        conn = dbutils.open_connection_with_scripting_account()
        cursor = conn.cursor() 
        cursor.fast_executemany = True
        print("Accessing File with id: ", id)
        print('Downloading file')
        try:  
            # Extraction Phase
            io_data = shwp.get_sharepoint_file_by_id(ctx, id)
            print("Data succesfully downloaded \nReading into dataframe")
            file_name = io_data['file_name']
            df = pd.read_csv(io_data["contents"], encoding="ISO-8859-1")
            try:
                df = df[SELECTED_COLUMNS]
            except Exception as e:
                raise Exception(f'File does not contain the expected columns review file with id: {id} Original error message: {e}')
            report_date = file_name.split('_')[0]
            report_date = datetime.strptime(report_date, "%m.%d.%y").date()

            ## Transformation Phase
            df = transfomation(df, HEADERS, PCT_COLUMNS ,report_date)

            print(df)
            # Loading Phase
            dbutils.perform_safe_delete_insert_with_keys(conn = conn, delete_keys=KEYS, source_df=df, schema=SCHEMA, target_table_name=TARGET_TABLE)           
            print("Moving to Historical Folder")
            shwp.move_file_to_folder(ctx, sh_config['folders'][FOLDER_KEY]['historical_id'], id)
            print("Correctly moved to historical folder")
        except Exception as e:
            print(e)
