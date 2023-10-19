"""
Downloads an Excel file containing productivity data from the SharePoint, uploads to the database and moves to archived.
"""

import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
import src.hrplus_sftp.transform_functions as transform_functions
from src.hrplus_sftp.configs import configs as script_configs
from office365.sharepoint.client_context import ClientContext
from multiprocessing.sharedctypes import Value

def extract_report_name(report_name_and_id: tuple) -> str:
    """It extracts the name of the hrplus report from all the title

    Args:
        report_name_and_id (tuple): (Name, Extension, ID)

    Returns:
        str: Name of the report e.g, Employee, EmpClockTimesheet.
    """
    name = report_name_and_id[0]
    name = name.split(".")[0]
    return name

def load_data_into_dataframe(file_extension: str, file_contents: str, use_cols: list, read_with_dtype) -> pd.DataFrame:
    """It loads the contents of the file into a pandas DataFrame.

    Args:
        file_extension (str): Extension of the file e.g, ".csv".
        file_contents (str): Contents of the file.
        use_cols (list): Columns to be used from the DataFrame.

    Raises:
        ValueError: The file has an invalid extension.

    Returns:
        DataFrame.
    """
    if file_extension == ".csv":
        df = pd.read_csv(file_contents, usecols=use_cols, dtype=read_with_dtype)
    elif file_extension == ".xlsx":
        df = pd.read_excel(file_contents)
    else:
        raise ValueError ("Invalid file extension")

    return df

def get_file_data_and_load_into_dataframe(ctx: ClientContext, file_to_load: tuple, use_cols: list, read_with_dtype, transform_function, case_config: dict) -> pd.DataFrame:
    """It gets the contents of the file to be loaded.

    Args:
        ctx (ClientContext): SharePoint connection.
        file_to_load (tuple): (Name, Extension, ID).
        use_cols (list): Columns to be used from the DataFrame.
        transform_function (function): Function to transform the DataFrame.
        case_config (dict): Dict with needed configurations for the DataFrame.

    Returns:
       DataFrame.
    """
    file_name_to_load = file_to_load[0]
    file_extension_to_load = file_to_load[1]
    file_id_to_load = file_to_load[2]
    file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id_to_load)
    file_contents_to_load = file_obj["contents"]
    print(f"LOADING '{file_name_to_load}' DATA INTO A DATAFRAME")
    df = load_data_into_dataframe(file_extension_to_load, file_contents_to_load, use_cols, read_with_dtype)
    df = transform_function(df, case_config)
    print(f"DATAFRAME CREATED!")
    return df

def truncate_insert_and_move_no_needed_files(filtered_files: list, conn, schema: str, table_name: str, use_cols: list, read_with_dtype, transform_function, ctx, case_config: dict, historical_folder_id):
    """It performs a safe truncate and insert with the most recent file and then moves all the files of the report name.

    Args:
        filtered_files (list): List of files that contain only the specified reports (case_name).
        conn (_type_): Database connection.
        schema (str): Database schema.
        table_name (str): Name of the table within the database.
        use_cols (list): Columns to be used.
        transform_function (_type_): Function to transform the DataFrame.
        ctx (_type_): SharePoint connection.

        case_config (_type_): Dict with configurations.
        historical_folder_id (_type_): Folder ID where all the used reports will be stored.
    """
    file_to_load = filtered_files[-1]
    df = get_file_data_and_load_into_dataframe(ctx, file_to_load, use_cols, read_with_dtype, transform_function, case_config)
    dbutils.perform_safe_truncate_insert(df, conn, schema, table_name)
    for file_to_move in filtered_files:
        file_to_move_name = file_to_move[0]
        file_to_move_id = file_to_move[2]
        print(f"Moving {file_to_move_name} to Historical Folder")
        shwp.move_file_to_folder(ctx, historical_folder_id, file_to_move_id)


def delete_insert_and_move_files(filtered_files, ctx, use_cols, read_with_dtype, transform_function, case_config, conn, delete_keys, schema, table_name, historical_folder_id):
    try:
        all_dfs = []
        cont = 1
        for file_to_load in filtered_files:
            print(f"File #{cont}")
            df = get_file_data_and_load_into_dataframe(ctx, file_to_load, use_cols, read_with_dtype, transform_function, case_config)
            all_dfs.append(df)
            cont += 1
        final_df = pd.concat(all_dfs)
        final_df.drop_duplicates(inplace=True)
        print(final_df)
        dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, final_df, schema, table_name)
        for file_to_move in filtered_files:
            file_to_move_id = file_to_move[2]
            print(f"MOVING {file_to_move[0]}")
            shwp.move_file_to_folder(ctx, historical_folder_id, file_to_move_id)
    except ValueError as e:
        print(f"It was not possible to upload the data: {e}")

def sheet_downloader_and_uploader(case_name: str, file_type:str, mode:str , delete_keys:list = None):
    """
    Reads all productivity Excel files in the folder and deletes and uploads to the database.
    Args:
        table_name (str): The name of the table to upload to.
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        folder_key (str): Name of the key of the folder in sharepoint.
    """

    print("Getting SharePoint context.")
    ctx = shwp.get_datascience_hub_ctx()
    hrplus_folder_id = utils.get_config("dshub_sharepoint_config")["folders"]["glb_hrplus_sftp"]["id"]
    sorted_files_names_extensions_and_ids = shwp.get_files_names_extensiones_and_ids_by_folder_id(ctx, hrplus_folder_id)
    case_config = script_configs[case_name]
    config = utils.get_config("dshub_sharepoint_config")["folders"][case_config["sharepoint_config_key"]]
    report_name = case_config["report_name"]
    filtered_files = list(filter(lambda x: extract_report_name(x) == report_name, sorted_files_names_extensions_and_ids))
    historical_folder_id = config["historical_id"]
    schema = config["schema"]
    table_name = config["target_table"]
    use_cols = case_config["use_cols"]
    read_with_dtype = case_config["read_with_dtype"]
    transform_function = case_config["transform_fn"]
    print(f"Running script for {case_name}")
    if len(filtered_files) >= 1:
        print(f"{len(filtered_files)} '{report_name}' FILES FOUND IN THE FOLDER")
        try:
            print("Opening database connection.")
            conn = dbutils.open_connection_with_scripting_account()
            if mode == "truncate":
                truncate_insert_and_move_no_needed_files(filtered_files, conn, schema, table_name, use_cols, read_with_dtype, transform_function, ctx, case_config, historical_folder_id)
            elif mode == "delete_insert":
                delete_insert_and_move_files(filtered_files, ctx, use_cols, read_with_dtype, transform_function, case_config, conn, delete_keys, schema, table_name, historical_folder_id)
            else:
                raise ValueError("Invalid mode of operation.")
        except Exception as e:
            conn.rollback()
            print("Table not uploaded, rolling back to previous state \n Error Details: ", e)
    else:
        print(f"No '{report_name}' Files found in the folder.")


def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode.
    """

    match optional[0]:
        case 1:
            case_name = "employees"
            sheet_downloader_and_uploader(case_name, file_type = 'csv', mode = 'truncate')
        case 2:
            case_name = "time_sheet"
            sheet_downloader_and_uploader(case_name, file_type = 'csv', mode = 'delete_insert', delete_keys=['dayWorked', "is_archived"])
        case 3:
            case_name = "positions"
            sheet_downloader_and_uploader(case_name, file_type = 'csv', mode = 'truncate')
        case 4:
            case_name = "emp_email"
            sheet_downloader_and_uploader(case_name, file_type = 'csv', mode = 'truncate')
        case 5:
            case_name = "hri_users"
            sheet_downloader_and_uploader(case_name, file_type = 'csv', mode = 'truncate')
        case 6:
            case_name = "time_sheet_arc"
            sheet_downloader_and_uploader(case_name, file_type = 'csv', mode = 'delete_insert', delete_keys=['dayWorked'])
        case 7:
            case_name = "reports_to"
            sheet_downloader_and_uploader(case_name, file_type = 'csv', mode = 'truncate')