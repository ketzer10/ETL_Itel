""" 
Downloads an Excel file containing productivity data from the SharePoint, uploads to the database and moves to archived.
"""

from pickle import FALSE
from unittest import skip

from numpy import number
import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
from src.office_depot.config.report_manager_config import configs
pd.options.mode.chained_assignment = None  

def transformations(df, expected_columns):     
    #blank_df = df.loc[df.isnull().all(1)]
    #if len(blank_df) > 0:
        #first_blank_index = blank_df.index[0]
        #df = df[:first_blank_index]

    df.drop(columns= ["PostedCalls5", "Textbox46", "Textbox48", "LockedCalls6", "Textbox39", "Textbox41", "Textbox24", "Textbox117", 
                     "HalfHourOfDay3", "PostedCalls9", "Textbox213", "Textbox214", "LockedCalls10", "ActualCalls4", "Textbox215", 
                     "Textbox216", "PostedHead7", "Textbox217", "LockedHead6", "Textbox218", "ActualTm11", "Textbox219", "ActualHead12", 
                     "ActualHead13", "Textbox220", "ActualAbnAll6"], inplace = True)
    df.columns = expected_columns
    df.dropna(subset = ["channel"],inplace = True)
    df.drop_duplicates(["channel", "date"], inplace = True)
    df["date"] = df["date"].astype("datetime64[ns]")

    number_columns = ["posted_volume", "uncommited_volume",  
                        "locked_volume", "actual_volume_offered", "actual_volume_answered", "volume_variance", 
                        "posted_hc", "variance_posted_hc", "locked_hc_avg", "locked_staff_hours", 
                        "locked_staff_hr_connected_available", "variance_staff_hours", "actual_calculated_hc", 
                        "variance_calculated_hc", "abandons"]

    df = dfutils.validate_float_columns(df, number_columns, 'coerce')
    df = dfutils.fill_dataframe_nulls(df)

    return df

def sheet_downloader_and_uploader(folder_key: str, delete_insert_keys: list, file_ext: str, read_with_dtype: str, qa_lob:str, skiprows = 0):
    """
    Reads all productivity Excel files in the folder and deletes and uploads to the database. 
    Args:        
        table_name (str): The name of the table to upload to. 
        output_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        folder_key (str): Name of the key of the folder in sharepoint.
    """

    print("Getting SharePoint context.")
    ctx = shwp.get_datascience_hub_ctx() 

    folder_id = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]["id"]
    historical_folder_id = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]["historical_id"]
    schema = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]["schema"]
    table_name = utils.get_config("dshub_sharepoint_config")["folders"][folder_key]["target_table"]

    print(f"Running script for {folder_key}: {folder_id}")       
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id=folder_id)     

    for file_id in file_ids:
        print("Accessing File with id: ", file_id)
        print("Downloading file")
        try:
            print("Opening database connection.")
            conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
            cursor = conn.cursor()                                                                                   
            cursor.fast_executemany = True            
            io_data = shwp.get_sharepoint_file_by_id(ctx, file_id)
            print(io_data['file_name'])
            print("Data successfully downloaded \nReading into dataframe")
            
            match file_ext:
                case "csv":
                    df = pd.read_csv(io_data['contents'], skiprows=skiprows, dtype=read_with_dtype, on_bad_lines = 'skip')
                case "xlsx":
                    df = pd.read_excel(io_data['contents'], skiprows=skiprows, dtype = read_with_dtype)

            print("Loaded to df", df.shape)
            print("Headers", df.columns.to_list())  

            # Transform dataframe
            df = configs[folder_key]["transform_function"](df, configs[folder_key]["info_transform_function"])           

            # Upload to database
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_insert_keys, df, schema, table_name)

            # Moving to Historical Folder
            print("Moving to Historical Folder")
            shwp.move_file_to_folder(ctx, historical_folder_id, file_id)
            print("Correctly moved to historical folder")            

        except Exception as e:
            conn.rollback()
            print("Table not uploaded, rolling back to previous state \n Error Details: ", repr(e))
        pass 


def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """    
    qa_lob = ''
    match optional[0]:
        case 0:    
            folder_key = "office_depot_geo_actual_forecast"
            file_ext = "csv"
            skiprows = 0
        case 1:
            folder_key = "office_depot_external_qa_billing"
            file_ext = "csv"
            skiprows = 0
        case 2:
            folder_key = "office_depot_external_qa_bsd"
            file_ext = "csv"
            skiprows = 0
        case 3:
            folder_key = "office_depot_external_qa_chat"
            file_ext = "csv"
            skiprows = 0
        case 4:
            folder_key = "office_depot_external_qa_contract"
            file_ext = "csv"
            skiprows = 0
        case 5:
            folder_key = "office_depot_external_qa_direct"
            file_ext = "csv"
            skiprows = 0                                              
        case 6:
            folder_key = "office_depot_external_qa_ecom"
            file_ext = "csv"
            skiprows = 0
        case 7:    
            folder_key = "office_depot_team_time"
            file_ext = "csv"
            skiprows = 0
        case 8:
            folder_key = "office_depot_cjp_calls_handled_queue"
            file_ext = "csv"
            skiprows = 0
        case 9:
            folder_key = "office_depot_cjp_agent_summary"
            file_ext = "csv"
            skiprows = 0
        case 10:
            folder_key = "od_crm_daily_chat"
            file_ext = "csv"
            skiprows = 0
        case 11:
            folder_key = "od_crm_daily_phone"
            file_ext = "csv"
            skiprows = 0
        case 12:
            folder_key = "od_crm_daily_sms"
            file_ext = "csv"
            skiprows = 0                         

    read_with_dtype = configs[folder_key]["read_with_dtype"]
    delete_insert_keys = configs[folder_key]["delete_insert_keys"]
    sheet_downloader_and_uploader(folder_key=folder_key, 
                                  delete_insert_keys=delete_insert_keys, 
                                  file_ext=file_ext, 
                                  skiprows=skiprows, 
                                  read_with_dtype=read_with_dtype, 
                                  qa_lob=qa_lob)