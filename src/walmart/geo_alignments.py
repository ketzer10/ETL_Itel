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

    expected_columns = ['WM ID', 'Agent name', 'VCC ID', 'EID', 'Supervisor']
     
    file_key = "wm_geo_alignments"
        
    data = sheet_downloader(expected_columns, file_key)
    df = transformations(data, expected_columns)

    df = dfutils.fill_dataframe_nulls(df)

    print(df)
    print(df.dtypes)

    cnxn = dbutils.open_connection_with_scripting_account()

    SCHEMA, TARGET_TABLE, DELETE_KEY = load_data_parameters(file_key)

    dbutils.perform_safe_delete_insert_with_keys(cnxn, DELETE_KEY, df, SCHEMA, TARGET_TABLE)

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

    df = pd.read_excel(data["contents"], sheet_name="Alignment")

    return df

def load_data_parameters(file_key):

    conditions_dictionary = utils.get_config("dshub_sharepoint_config")["files"][file_key]

    schema = conditions_dictionary["schema"]
    target_table = conditions_dictionary["target_table"]
    delete_key = conditions_dictionary['delete_key']

    return schema, target_table, delete_key

def transformations(df, expected_columns):

    df = df[expected_columns]

    names_dir = {'EID': 'emp_id',
                'Agent name': 'full_name',
                'Supervisor': 'supervisor',
                'VCC ID': 'vccid',
                'WM ID': 'wm_login'}
    
    df = df.rename(columns=names_dir)

    df = df[df['emp_id'].notna()]
    df = df[df['vccid'].notna()]

    df['emp_id'] = df['emp_id'].astype(int)
    df['emp_id'] = df['emp_id'].astype(str)

    df['vccid'] = df['vccid'].astype(int)
    df['vccid'] = df['vccid'].astype(str)

    df['site'] = 'Guyana'
    df['account'] = 'Walmart'
    df['bpo_wah'] = 'NULL'
    df['status'] = 'NULL'
    df['stage'] = 'NULL'
    df['position'] = 'NULL'
    df['manager'] = 'NULL'
    df['lob'] = 'NULL'
    df['connection_type'] = 'NULL'
    df['language'] = 'NULL'
    df['work_email'] = 'NULL'
    df['wave'] = 'NULL'
    df['hire_date'] = 'NULL'
    df['nstg_date'] = 'NULL'
    df['prod_date'] = 'NULL'
    df['transferred_to'] = 'NULL'
    df['transferred_from'] = 'NULL'
    df['transfer_date'] = 'NULL'
    df['attri_date'] = 'NULL'
    df['attrition_type'] = 'NULL'
    df['attrition_reason'] = 'NULL'

    df = df[['bpo_wah', 'site', 'account', 'emp_id', 'status', 'stage', 'position', 'full_name', 'supervisor', 'manager',
                'lob', 'connection_type', 'language', 'vccid', 'wm_login', 'work_email', 'wave', 'hire_date',
                'nstg_date', 'prod_date', 'transferred_to', 'transferred_from', 'transfer_date', 'attri_date',
                'attrition_type', 'attrition_reason']]

    return df
