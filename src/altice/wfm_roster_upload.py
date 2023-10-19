""" 
Downloads an Excel file containing roster alignment for Altice from WFM.
"""

import utils.dbutils as dbutils
import pandas as pd
import numpy as np
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
from src.altice.config.altice_wfm_roster_configs import sheets_configs
from src.altice.config.altice_wfm_roster_configs import final_cols


def order_full_name(name):
    full_name = name.split(", ")
    if len(full_name) > 1:
        last_name = full_name[0]
        first_name = full_name[1]
        return f"{first_name} {last_name}"
    else:
        return name

def sheet_downloader_and_uploader(folder_id: str, historical_id: str, final_cols: list, schema: str, table: str):
    """Truncates and uploads a forecast live Excel files to the database. 
    Args:
        table_name (str): The name of the table to upload to. 
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        file_id (str): ID for the file in sharepoint
        sheet_name (str): Optional argument that specifies the sheet name. Only one sheet name can be passed. If no argument 
        is passed, the first sheet of the Excel workbook is read.
    """

    print('Getting SharePoint context.')
    ctx = shwp.get_datascience_hub_ctx()
    print('Getting file from SharePoint site.')
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id)
    try:
        all_dfs = []
        for file_id in file_ids:
            for sheet in sheets_configs.keys():
                conf = sheets_configs[sheet]
                sheet_name = conf["sheet_name"]
                use_cols = conf["use_cols"]
                to_rename_cols = conf["to_rename_cols"]
                date_cols = conf["date_cols"]
                read_dtypes = conf["read_dtypes"]
                name_cols = conf["name_cols"]
                to_add_columns = conf["to_add_columns"]
                file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id)
                df = pd.read_excel(file_obj['contents'], sheet_name=sheet_name, usecols=use_cols, dtype=read_dtypes)
                df = dfutils.validate_text_columns(df, name_cols)
                df = dfutils.validate_date_columns(df, date_cols, date_format="%Y-%m-%d")
                for name_col in name_cols:
                    df[name_col] = df[name_col].apply(order_full_name)
                df.rename(columns=to_rename_cols, inplace=True)
                for col in to_add_columns:
                    df[col] = np.nan
                df = dfutils.fill_dataframe_nulls(df)
                df = df.reindex(columns=final_cols)
                df["ewfm_id"] = df["ewfm_id"].str.strip("_")
                df["hrm_id"] = df["hrm_id"].str.strip()
                print(df)
                all_dfs.append(df)
                
            df_to_upload = pd.concat(all_dfs, ignore_index=True)
            print(df_to_upload)
            print('Opening database connection.') # Get Data Science Hub SharePoint context
            conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
            dbutils.perform_safe_truncate_insert(df_to_upload, conn, schema, table)
            shwp.move_file_to_folder(ctx, historical_id, file_id)
    except Exception as e:
        print(f"Something went wrong: {e}")


def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """

    match optional[0]:
        case 1:
            """
            Read, transform and upload data from WFM Roster Altice in Sharepoint to iteldsi
            """
            ds_conf = utils.get_config('dshub_sharepoint_config')['folders']['wfm_roster_altice']
            folder_id = ds_conf['id']
            historical_id = ds_conf["historical_id"]
            schema = ds_conf["schema"]
            table = ds_conf["target_table"]
            sheet_downloader_and_uploader(folder_id, historical_id, final_cols, schema, table)