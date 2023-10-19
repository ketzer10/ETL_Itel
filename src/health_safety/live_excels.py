""" 
Downloads an Excel file containing forecasts from the SharePoint and uploads to the database.  
"""

import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
from src.health_safety.config.config_files import configs

def sheet_downloader_and_uploader(sheet_name: str, table_name: str, schema: str, file_id: str, read_with_dtype: dict, transform_function, info_transform_function: str):
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
    df = transform_function(df, info_transform_function)

    # Fill empty values with NULLS 
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
        # Form data 
        case 1:
            FOLDER_KEY = "bus_arrival_departure_log"
            transform_function = configs[FOLDER_KEY]["transform_function"]
            info_transform_function = configs[FOLDER_KEY]["info_transform_function"]
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            sheet_name = "Cleaned_Form"
            table_name = "bus_arrival_departure_log"
            schema = "environmental_health_safety"
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["transporation_form_arrival_departure_log"]["id"]
        # Car data          
        case 2:
            FOLDER_KEY = "vehicle_capacities"
            transform_function = configs[FOLDER_KEY]["transform_function"]
            info_transform_function = configs[FOLDER_KEY]["info_transform_function"]
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            sheet_name = "Vehicle Capacity"
            table_name = "vehicle_capacities"
            schema = "environmental_health_safety"
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["transportation_car_capacity_rates"]["id"]
        # Trip rate data          
        case 3:
            FOLDER_KEY = "trip_costs"
            transform_function = configs[FOLDER_KEY]["transform_function"]
            info_transform_function = configs[FOLDER_KEY]["info_transform_function"]
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            sheet_name = "Costs"
            table_name = "trip_costs"
            schema = "environmental_health_safety"
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["transportation_car_capacity_rates"]["id"]

        # Honduras Cost

        case 4:
            FOLDER_KEY = "honduras_trip_cost"
            transform_function = configs[FOLDER_KEY]["transform_function"]
            info_transform_function = configs[FOLDER_KEY]["info_transform_function"]
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            sheet_name = "Consolidated"
            table_name = "honduras_trip_cost"
            schema = "environmental_health_safety"
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["honduras_trip_cost"]["id"]

    print(f"Running script for {schema}.{table_name} from {sheet_name}")
    sheet_downloader_and_uploader(
        sheet_name = sheet_name, 
        table_name= table_name, 
        schema = schema, 
        file_id = file_id, 
        read_with_dtype = read_with_dtype, 
        info_transform_function = info_transform_function, 
        transform_function = transform_function)