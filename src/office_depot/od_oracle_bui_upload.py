import pandas as pd
import numpy as np
from src.office_depot.config.oracle_bui_config import  configs
from src.office_depot.functions.oracle_bui_functions import create_df
from utils.sharepoint_wrapper import get_datascience_hub_ctx, get_files_names_extensiones_and_ids_by_folder_id, move_file_to_folder
from utils.utils import get_config
from utils.dfutils import validate_date_columns, fill_dataframe_nulls
from utils.dbutils import open_connection_with_scripting_account, perform_safe_delete_insert_with_keys

def download_and_upload_Oracle_BUI_data(case_name: str):
    """It downloads the data from the files in the OD Oracle BUI folders, upload it into the itel dsi database and finally moves the files
    to the Historical Document library.

    Args:
        case_name (str): Name to be used to get necessary info from the configs dictionary (configs from oracle_bui_config)
    """
    print("Getting sharepoint context.")
    ctx = get_datascience_hub_ctx()
    case_config = configs[case_name]
    config = get_config("dshub_sharepoint_config")["folders"][case_config["sharepoint_config_key"]]
    folder_id = config["id"]
    folder_name = config["name"]
    historical_folder_id = config["historical_id"]
    schema = config["schema"]
    table_name = config["target_table"]
    all_files = get_files_names_extensiones_and_ids_by_folder_id(ctx, folder_id)
    if len(all_files) == 0:
        print("No files found.")
    else:
        print(f"{len(all_files)} FILES FOUND FOR {case_name}")
        num_columns = case_config["num_columns"]
        skiprows = case_config["skiprows"]
        skip_last_rows = case_config["skip_last_rows"]
        extract_date_from_file_name_function = case_config["extract_date_from_file_name_function"]
        need_seesionid_column = case_config["need_sessionid_column"]
        columns_to_use = case_config["columns_to_use"]
        site_column = case_config["site_column"]
        itel_references = case_config["itel_references"]
        agent_column = case_config["agent_column"]
        get_agent_name_function = case_config["get_agent_name_function"]
        date_column = case_config["date_column"]
        new_columns_name = configs["general"]["new_columns_names"]["for_incidents"] if extract_date_from_file_name_function else configs["general"]["new_columns_names"]["for_errors"]
        delete_keys = configs["general"]["delete_keys"]
        try:
            df = create_df(all_files, ctx, skiprows, skip_last_rows, num_columns, extract_date_from_file_name_function)
            print("Transforming total dataframe.")
            if need_seesionid_column:
                print("Creating SessionID Column.")
                df["SessionID"] = np.nan
            print("Selecting needed columns.")
            df = df[columns_to_use]
            print(f"Filtering by sites: {itel_references}")
            df = df[df[site_column].isin(itel_references)]
            print(f"Filtering out rows with nan AgentName column values")
            df = df[~df[agent_column].isna()]
            if get_agent_name_function:
                print("Extracting AgentName from email.")
                df[agent_column] = df[agent_column].apply(get_agent_name_function)
            df[date_column] = pd.to_datetime(df[date_column]).dt.date
            print("Inserting ReportName column.")
            df.insert(0, "ReportName", case_name)
            df.columns = new_columns_name
            df = validate_date_columns(df, columns=["date"], date_format="%Y-%m-%d")
            df = fill_dataframe_nulls(df)
            print("Dataframe is ready to be uploaded!")
            print("Opening database connection.")
            conn = open_connection_with_scripting_account()
            perform_safe_delete_insert_with_keys(conn, delete_keys, df, schema, table_name)
            for file in all_files:
                file_name = file[0]
                file_id = file[2]
                print(f"Movig {file_name} to Historical folder")
                move_file_to_folder(ctx, historical_folder_id, file_id)
            
        except ValueError as e:
            print(f"It was not possible to upload the data: {e}")


def main(optional: list):
    """ Runs the download_and_upload_Oracle_BUI_data function.
    Args:
        optional (int): Run mode. 
    """
    
    match optional[0]:
        case 0:
            case_name = "Cisco_BUI_Oracle_assigned"
            download_and_upload_Oracle_BUI_data(case_name)
        case 1:
            case_name = "Dir_Phone_Agents_no_using_Order_Lookup"
            download_and_upload_Oracle_BUI_data(case_name)
        case 2:
            case_name = "Incidents_Cisco_BUI_Invalid_Email"
            download_and_upload_Oracle_BUI_data(case_name)
        case 3:
            case_name = "ODPB_Email_Agents_no_using_Order_Lookup"
            download_and_upload_Oracle_BUI_data(case_name)
        case 4:
            case_name = "Sites_Agents_not_saving_the_incident"
            download_and_upload_Oracle_BUI_data(case_name)