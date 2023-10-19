import utils.dbutils as dbutils
import pandas as pd
import numpy as np
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
from src.walmart.config.wm_wfm_roster_configs import roster_configs

def sheet_downloader_and_uploader(folder_id: str, historical_id: str, schema: str, table: str):
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
    files = shwp.get_files_names_extensiones_and_ids_by_folder_id(ctx, folder_id)
    try:
        all_dfs = []
        for file in files:
            file_name = file[0]
            file_id = file[2]
            sheet_name = roster_configs["sheet_name"]
            use_cols = roster_configs["use_cols"]
            read_dtypes = roster_configs["read_dtypes"]
            rename_cols = roster_configs["rename_cols"]
            date_cols = roster_configs["date_cols"]
            replace_dash = roster_configs["replace_dash"]
            final_cols = roster_configs["final_cols"]
            file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id)
            print(f"Loading {file_name} onto a DataFrame")
            df = pd.read_excel(file_obj['contents'], sheet_name=sheet_name, usecols=use_cols, dtype=read_dtypes)
            for col in replace_dash:
                df[col] = df[col].replace("-", np.nan)
            df = dfutils.validate_date_columns(df, date_cols, date_format="%Y-%m-%d")
            df.rename(columns=rename_cols, inplace=True)
            df = dfutils.fill_dataframe_nulls(df)
            df = df.reindex(columns=final_cols)
            print(df)
            all_dfs.append(df)
                
        df_to_upload = pd.concat(all_dfs, ignore_index=True)
        print("This is the final DataFrame to upload!")
        print(df_to_upload)
        print('Opening database connection.') # Get Data Science Hub SharePoint context
        conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
        dbutils.perform_safe_truncate_insert(df_to_upload, conn, schema, table)
        print(f"Moving {file_name} to the Historical folder")
        # shwp.move_file_to_folder(ctx, historical_id, file_id)
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
            Read, transform and upload data from WFM Roster Walmart in Sharepoint to iteldsi
            """
            ds_conf = utils.get_config('dshub_sharepoint_config')['folders']['wfm_roster_walmart']
            folder_id = ds_conf['id']
            historical_id = ds_conf["historical_id"]
            schema = ds_conf["schema"]
            table = ds_conf["target_table"]
            sheet_downloader_and_uploader(folder_id, historical_id, schema, table)