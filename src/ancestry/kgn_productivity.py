"""
KGN Productivity Data for Ancestry 

CMD command: python run.py -i 44 -o [1, 2, 3, 4, 5]
"""
from tracemalloc import start

from numpy import record
from src.ancestry.config.kng_producticity_config_files import configs
from asyncio import exceptions
import utils.sharepoint_wrapper as shwp
import utils.dbutils as dbutils
import utils.dfutils as dfutils
import pandas as pd
import numpy as np

def pipeline(folder_key: str, folder_information: dict, save_information: dict, read_information: str, transform_function, info_transform_function: dict):
    # Getting the contex
    print("Getting SharePoint context")
    ctx = shwp.get_datascience_hub_ctx()   

    # Getting files IDs from the folder
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id = folder_information["folder_id"])
    for id in file_ids:
        print("Accessing File with id: ", id)
        print('Downloading file')

        try:  
            # Extraction Phase
            io_data = shwp.get_sharepoint_file_by_id(ctx, id)
            print(io_data['file_name'])
            print("Data succesfully downloaded")
            print("Reading into dataframe")

            df = pd.read_excel(io_data["contents"], dtype = read_information["read_with_dtype"])
            if folder_key == "agent_snapshop":
                firt_row_agent_snapshop = any(item in df.columns for item in read_information["read_with_dtype"].keys())
                if firt_row_agent_snapshop == False:   # some file for ancestry_snapshot firts row not contain the header
                    df = pd.read_excel(io_data["contents"], header = 1, dtype = read_information["read_with_dtype"])

            # data handling phase
            df = transform_function(df, info_transform_function, file_name = io_data['file_name'])
            df = dfutils.fill_dataframe_nulls(df, "")

            print(df)
            # print(None in df['record_id'].unique())
            # print(df[df["record_id"] == "1287"])
            # for colum in ["date", "record_id"]:#df.columns:
            #     print(colum)
            #     print(None in df[colum].unique())
            # print(df[df["start_time"] == np.nan])
            # print("---")
            # print(df[df["end_time"] == None])
            # print("---")
            # print(df[df["date"] == None])
            # print(df)

            # Creating Database connection
            print("Opening connection to database")
            conn = dbutils.open_connection_with_scripting_account()
            cursor = conn.cursor() 
            cursor.fast_executemany = True


            # Loading Phase
            try:
                print("Loading data into database")
                dbutils.perform_safe_delete_insert_with_keys(
                    conn = conn, 
                    delete_keys = save_information["delete_keys"], 
                    source_df = df, 
                    schema = save_information["schema"], 
                    target_table_name = save_information["target_table"]
                )
                if folder_key not in ["sys_issues", "coaching_fs_meeting"]:
                    print("Moving to Historical Folder")
                    try:
                        print("Moving to Historical Folder")
                        shwp.move_file_to_folder(ctx, folder_information["folder_historical_id"], id)
                        print("Correctly moved to historical folder")
                    except Exception as e:
                        print(f"ERROR: {e}")
                    pass 
            except Exception as e:
                print(f"ERROR: {e}")     

        except Exception as e:
            print(e)


def main(optional: list):
    
    match optional[0]:
        case 1:
            # Getting Configs
            folder_key = "agent_snapshop"
            folder_information = configs[folder_key]["folder_information"]
            save_information = configs[folder_key]["save_information"]
            read_information = configs[folder_key]["read_information"]
            transform_function =  configs[folder_key]["transform_function"]
            info_transform_function = configs[folder_key]["info_transform_function"]
        case 2:
            # Getting Configs
            folder_key = "agent_time_card"
            folder_information = configs[folder_key]["folder_information"]
            save_information = configs[folder_key]["save_information"]
            read_information = configs[folder_key]["read_information"]
            transform_function =  configs[folder_key]["transform_function"]
            info_transform_function = configs[folder_key]["info_transform_function"]
        case 3:
            # Getting Configs
            folder_key = "coaching_fs_meeting"
            folder_information = configs[folder_key]["folder_information"]
            save_information = configs[folder_key]["save_information"]
            read_information = configs[folder_key]["read_information"]
            transform_function =  configs[folder_key]["transform_function"]
            info_transform_function = configs[folder_key]["info_transform_function"]
        case 4:
            # Getting Configs
            folder_key = "sys_issues"
            folder_information = configs[folder_key]["folder_information"]
            save_information = configs[folder_key]["save_information"]
            read_information = configs[folder_key]["read_information"]
            transform_function =  configs[folder_key]["transform_function"]
            info_transform_function = configs[folder_key]["info_transform_function"]
        case 5:
            # Getting Configs
            folder_key = "unavailable_time"
            folder_information = configs[folder_key]["folder_information"]
            save_information = configs[folder_key]["save_information"]
            read_information = configs[folder_key]["read_information"]
            transform_function =  configs[folder_key]["transform_function"]
            info_transform_function = configs[folder_key]["info_transform_function"]

    pipeline(folder_key, folder_information, save_information, read_information, transform_function, info_transform_function)



    # j#eerors
    # 4.19.2022 IC_Reports_AgentUnavailableTime (38).xlsx
    # 4.16.2022 IC_Reports_AgentUnavailableTime (38).xlsx
    # 12.9-.2021-IC_Reports_AgentUnavailableTime (20).xlsx

    # 3.11.2022AgentTimeCard (16).xlsx
    # AgentTimeCard (41).xlsx
    # April.19.2022AgentTimeCard (22).xlsx
    # 4.19.2022AgentTimeCard.xlsx
    # Agent Time Card - Acum - 031622.xlsx
    # 3.20.2022AgentTimeCard (17).xlsx
    # 4.13.2022-AgentTimeCard (16).xlsx
    # Apr.11.2022-AgentTimeCard (16).xlsx
    # 12.13.2021AgentTimeCard (16).xlsx
    # AgentTimeCard (43).xlsx
    # AgentTimeCard (38).xlsx
    # 12.14.2021AgentTimeCard (16).xlsx
    # April.14.2022AgentTimeCard (22).xlsx
    # AgentTimeCard (40).xlsx
    # AgentTimeCard (42).xlsx
    # 

            # print(None in df['record_id'].unique())
            # print(df[df["record_id"] == "1287"])
            # for colum in df.columns:
            #     print(colum)
            #     print(df[colum].unique())
            # print(df[df["start_time"] == np.nan])
            # print("---")
            # print(df[df["end_time"] == None])
            # print("---")
            # print(df[df["date"] == None])
            # print(df)














