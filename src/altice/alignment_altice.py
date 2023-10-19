""" 
Downloads an Excel file containing aligment from the SharePoint and uploads to the database.
"""

import pandas as pd
import numpy as np

import utils.dbutils as dbutils
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """    

    expected_columns = ['ps_id', 'report_agent_name', 'hrm_id']
     
    file_key = "altice_alignments"
        
    data = sheet_downloader(expected_columns, file_key)
    df = transformations(data, expected_columns)

    print(df)

    cnxn = dbutils.open_connection_with_scripting_account()

    SCHEMA, TARGET_TABLE = load_data_parameters(file_key)

    load_data = dbutils.perform_safe_truncate_insert(df, cnxn, SCHEMA, TARGET_TABLE)

    return df

def sheet_downloader(expected_columns: list, file_key: str):
    """
    Reads alignment Excel file in the folder and deletes and uploads to the database. 
    Args:        
        table_name (str): The name of the table to upload to. 
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        file_key (str): Name of the key of the folder in sharepoint.
    """

    print("Getting SharePoint context.")
    ctx = shwp.get_datascience_hub_ctx() 

    file_id = utils.get_config("dshub_sharepoint_config")["files"][file_key]["id"]
    file_name = utils.get_config("dshub_sharepoint_config")["files"][file_key]["name"]

    print(f"Running script for {file_key}: {file_id}")       
    data = shwp.get_sharepoint_file_by_id(ctx, file_id = file_id)

    df = pd.read_excel(data["contents"], sheet_name="PS_ID_HRM_ID")

    return df

def load_data_parameters(file_key):

    schema = utils.get_config("dshub_sharepoint_config")["files"][file_key]["schema"]
    target_table = utils.get_config("dshub_sharepoint_config")["files"][file_key]["target_table"]

    return schema, target_table

def transformations(df, expected_columns):

    df = df[expected_columns]
    df = df.dropna(subset=['hrm_id'])
    df['hrm_id'] = df['hrm_id'].astype(str) 
    df["hrm_id"] = df["hrm_id"].apply(lambda txt: txt.split(".")[0]) 

    return df
