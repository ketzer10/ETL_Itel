from os import rename
import pandas as pd
from scheduling.sch_handling_functions_lib import altice_sched_handling
import utils.dfutils as dfutils
import utils.dbutils as dbutils
import utils.utils as utils 
import utils.sharepoint_wrapper as shwp
#import src.scheduling.configs as sched_configs

date_format="%Y-%m-%d"
time_format="%H:%M:%S"

def sheet_downloader_and_uploader(config:dict, lob:str, folder_key):
    file_type = config["file_type"]
    skiprows = config["skiprows"]
    date_columns = config["date_columns"]
    time_columns = config["time_columns"]
    handling_function = config["handling_function"]
    output_columns = config["output_columns"]
    expected_columns = config["expected_columns"]
    
    print('Getting SharePoint context.')
    ctx = shwp.get_datascience_hub_ctx()
   
    folder_id = utils.get_config('dshub_sharepoint_config')['folders'][folder_key]['id']    
    historical_folder_id = utils.get_config('dshub_sharepoint_config')['folders'][folder_key]['historical_id']
    print(f"Running script for {folder_key}: {folder_id}")       
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id=folder_id)   

    for file_id in file_ids:
        print("Accessing File with id: ", file_id)
        print('Downloading file')
        try:
            print('Opening database connection.') # Get Data Science Hub SharePoint context
            conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
            cursor = conn.cursor()                                                                                   
            cursor.fast_executemany = True   

            file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
            print('Loading file into pandas DataFrame.')
            match file_type:
                case "csv":
                    df = pd.read_csv(file_obj['contents'], skiprows=skiprows)
                case "xlsx":
                    df = pd.read_excel(file_obj['contents'], skiprows=skiprows)
            
            match handling_function:
                case "altice_sched_handling":
                    code_remap_start = config["code_remap_start"]
                    code_remap_end = config["code_remap_end"]    
                    input_time_format = config["input_time_format"]
                    altice_sched_handling(df, expected_columns, rename_columns=config["rename_columns"])
        except Exception as e:
            conn.rollback()
            print('Table not uploaded, rolling back to previous state \n Error Details: ', e)
        pass             



def main(optional: list):
    match optional[0]:
        case 0:
            lob = "Altice SLU"
            config = utils.get_config_py("schedules_config_py")["files"][lob]
    
    file_type = config["file_type"]
    skiprows = config["skiprows"]
    sheet_downloader_and_uploader(config, lob)