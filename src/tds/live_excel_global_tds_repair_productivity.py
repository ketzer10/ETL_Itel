""" 
Global Productivity Data for TDS - Financial Services 
 
CMD comand -> python .\run.py -i 47 -o 1
"""

import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
from src.tds.config.config_files import configs

def sheet_downloader_and_uploader(file_id: str, sheet_name: str, read_with_dtype: dict, expected_columns: list, transform_function, info_transform_function: str, schema: str, table_name: str):
    """Truncates and uploads a forecast live Excel files to the database. 
    Args:
        sheet_name (str): The name of the sheet on the file to be uploaded.  
        table_name (str): The name of the table to upload to. 
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        file_id (str): ID for the file in sharepoint
    """
    print("Getting SharePoint context.")
    ctx = shwp.get_datascience_hub_ctx()
    print("Opening database connection.") # Get Data Science Hub SharePoint context
    conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
    print("Getting file from SharePoint site.")    
    file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
    print("Loading Excel file into pandas DataFrame.")
    df = pd.read_excel(file_obj["contents"], sheet_name=sheet_name, dtype = read_with_dtype) # Read into a DataFrame

    df = dfutils.stack_dfs(df.values(), expected_columns)

    # Verify that expected columns match the actual dataframe columns
    assert expected_columns == df.columns.tolist(), "Expected columns do not match actual dataframe columns"

    # Fill empty values with NULLS 
    df = transform_function(df, info_transform_function)
    df = dfutils.fill_dataframe_nulls(df, "")

    print(df)
    
    print("Truncating database and reinserting.")
    # Truncate and insert into the database
    dbutils.perform_safe_truncate_insert(df, conn, schema, table_name)

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """

    match optional[0]:
        case 1:
            FOLDER_KEY = "global_tds_repair_productivity"
            transform_function = configs[FOLDER_KEY]["transform_function"]
            info_transform_function = configs[FOLDER_KEY]["info_transform_function"]
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            sheet_name = None#"June"
            schema = "tds"
            table_name = "glb_repair_productivity"
            expected_columns = [
                "agent_id",
                "agent_name",
                "date",
                "quality_score",
                "would_hire",
                "average_handle",
                "repeat_tickets",
                "escalated_tickets",
                "supervisor",
                "operations_manager",
                "site",
                "location"
            ]
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["global_tds_repair_productivity"]["id"]
        
    print(f"Running script for {schema}.{table_name} from {sheet_name}")
    sheet_downloader_and_uploader(file_id, sheet_name, read_with_dtype, expected_columns, transform_function, info_transform_function, schema, table_name)