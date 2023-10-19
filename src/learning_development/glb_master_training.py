""" 
Downloads an Excel file containing productivity data from the SharePoint, uploads to the database and moves to archived.
"""

from datetime import datetime
from numpy import timedelta64
from requests import delete
import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils

def transformations(df, expected_columns, current_historical):
    df["current_historical_flag"] = ""
    match current_historical:
        case 1: df["current_historical_flag"] = "current"
        case 2: df["current_historical_flag"] = "historical"
   
    df.columns = expected_columns

    df.dropna(subset=["employee_name"],inplace=True)  
    df["employee_id"] = df["employee_id"].astype('str')
    df["employee_id"] = df["employee_id"].apply(lambda txt: txt.split(".")[0])   

    date_columns = ["class_start_date", "class_end_date"]
    float_columns = ["total_training_hours", "days_worked", "log_time", "attendance", "cs_exam", "combined_product_test", "wpm_testing", "wpm", "evaluation_score", "overall_score"]
    df = dfutils.validate_datetime_columns(df,date_columns,date_format="%Y-%m-%d")
    df = dfutils.validate_float_columns(df, float_columns)
    df = dfutils.fill_dataframe_nulls(df)

    return df

def sheet_downloader_and_uploader(expected_columns: list, folder_key: str, current_historical_flag: int):
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

    read_columns = ["Employee ID", "Employee Name", "Business Unit", "Site", "Line of Business", "Batch", "Class Start Date", 
                    "Class End Date", "Position/Role", "Total Training Hours (Scheduled)", "Days Worked", "Log Time", "Attendance", 
                    "CS Exam", "Combined Product Knowledge Test", "WPM Testing", "WPM %", "Evaluation Score", "Overall Score", 
                    "Graduated", "Learning Style(s)"] 

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
            file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
            print("Loading Excel file into pandas DataFrame.")
            df = pd.read_excel(file_obj["contents"], sheet_name=None) # Read into a Dictionary of DataFrame            
            dropped_sheets = ["Sample", "Site", "Key", "Data Science & Inn Req", "BAH", "SLU", "GUY", "HON", "WAH", "USA", "Sheet1"]
            combined_df = []
            print("Stacking sheets.")
            for sheet in df.keys():
                if sheet not in dropped_sheets:              
                    df_t = df[sheet].iloc[:,:21]                               
                    df_t.columns = read_columns
                    combined_df.append(df_t)  
            all_df = dfutils.stack_dfs(combined_df, read_columns)

            all_df.columns = all_df.columns.str.lower()
            all_df.columns = all_df.columns.str.replace(' ','_')

            print("Dataframe built from stacked sheets. Shape:", all_df.shape)

            # Transform dataframe
            df = transformations(all_df, expected_columns, current_historical_flag)    



            # Verify that expected columns match the actual dataframe columns
            assert expected_columns == df.columns.tolist(), "Expected columns do not match actual dataframe columns"
            
            df = df.rename(columns={
                'class_start_date':'training_start_date',
                'class_end_date':'training_end_date'
                })

            print(df.columns)   

            print("Opening database connection.") # Get Data Science Hub SharePoint context
            conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
            cursor = conn.cursor()                                                                                   
            cursor.fast_executemany = True
            delete_keys = ["current_historical_flag"]            
                    
            # Upload to database
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, df, schema, table_name)

            # Moving to Historical Folder
            #print("Moving to Historical Folder")
            #shwp.move_file_to_folder(ctx, historical_folder_id, file_id)
            #print("Correctly moved to historical folder")            

        except Exception as e:
            #conn.rollback()
            print("Table not uploaded, rolling back to previous state \n Error Details: ", e)
        pass 


def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """    
    match optional[0]:
        case 1:
            expected_columns = ["employee_id", "employee_name", "business_unit", "site", "lob", "batch", "class_start_date", 
                                "class_end_date", "position_role", "total_training_hours", "days_worked", "log_time", "attendance", 
                                "cs_exam", "combined_product_test", "wpm_testing", "wpm", "evaluation_score", "overall_score", "graduated", 
                                "learning_style", "current_historical_flag"]
            folder_key = "glb_master_training"
                
            sheet_downloader_and_uploader(expected_columns, folder_key, optional[0])
        case 2:
            expected_columns = ["employee_id", "employee_name", "business_unit", "site", "lob", "batch", "class_start_date", 
                                "class_end_date", "position_role", "total_training_hours", "days_worked", "log_time", "attendance", 
                                "cs_exam", "combined_product_test", "wpm_testing", "wpm", "evaluation_score", "overall_score", "graduated", 
                                "learning_style", "current_historical_flag"]
            folder_key = "glb_master_training_historical"
            sheet_downloader_and_uploader(expected_columns, folder_key, optional[0])