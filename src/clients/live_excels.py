""" 
Downloads an Excel file containing forecasts from the SharePoint and uploads to the database.  
"""

import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils

def sheet_downloader_and_uploader(sheet_name: str, table_name: str, expected_columns: list, schema: str, file_id: str):
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
    df = pd.read_excel(file_obj["contents"], sheet_name=sheet_name) # Read into a DataFrame

    # Verify that expected columns match the actual dataframe columns
    assert expected_columns == df.columns.tolist(), "Expected columns do not match actual dataframe columns"

    # Fill empty values with NULLS 
    df = dfutils.fill_dataframe_nulls(df, "")

    print("Truncating database and reinserting.")
    # Truncate and insert into the database
    dbutils.perform_safe_truncate_insert(df, conn, schema, table_name)

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """

    match optional[0]:
        # Form data cnps
        case 1:
            sheet_name = "cnps"
            schema = "clients"
            table_name = "customer_net_promoter_score"
            expected_columns = [
                "id", "email", "date",
                "most_valuable_in_the_partnership",
                "overall_satisfaction_with_our_services",
                "recommend_itels_services",
                "improve_one_thing",	
                "improve_your_experience_at_itel"
            ]
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["customer_net_promoter_score"]["id"]
        
    print(f"Running script for {schema}.{table_name} from {sheet_name}")
    sheet_downloader_and_uploader(sheet_name, table_name, expected_columns, schema, file_id)