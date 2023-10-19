"""
Productivity Data for Ancestry on KPI Dashboard 

CMD command: python run.py -i 52 -o [1, 2]
"""
from src.louis_vuitton.config.config_files import configs
import utils.sharepoint_wrapper as shwp
import utils.dbutils as dbutils
import utils.dfutils as dfutils
import pandas as pd

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
            if folder_key == "lv_glb_percent_on_queve":
                df = pd.read_excel(io_data["contents"], header = 8, dtype = read_information["read_with_dtype"])
                df.dropna(subset = ["Date"], inplace = True)
            elif folder_key == "lv_glb_quality_assessment":
                df = pd.read_excel(io_data["contents"])
                # df = df.melt(id_vars = [
                #     "ID", "Start time", "Completion time", "Email", "Name", "Team Manager",
                #     "Call Type2", "Month", "Date", "QA By", "Inbound Phone #", "Recording Date / Time", 
                #     "Duration", "Batch #", "Baseline Job Requirement is 90%"
                # ])
            elif folder_key == "lv_glb_service_level_requirement":
                df = pd.read_excel(io_data["contents"], header = 8, dtype = read_information["read_with_dtype"])
                df["Date"] = pd.to_datetime(df["Date"], exact = True, errors = 'coerce', format = "%m/%d/%y")
                df.dropna(subset = ["Date"], inplace = True)
            elif folder_key == "lv_glb_client_report":
                df = pd.read_excel(io_data["contents"], header = 2, dtype = read_information["read_with_dtype"], sheet_name = "1. CA Roster")
                df.dropna(subset = ["Genesys ID"], inplace = True)
                df["date"] = io_data['file_name'].split(" ")[1]
                df["date"] = pd.to_datetime(df["date"], exact = True, errors = 'coerce', format = "%m.%d.%y")

            # data handling phase
            df = transform_function(df, info_transform_function, file_name = io_data['file_name'])
            df = dfutils.fill_dataframe_nulls(df, "")

            print(df)
            # print(df.columns)
            # print(None in df['record_id'].unique())
            # print(df[df["record_id"] == "1287"])
            # for colum in ["base_job_requirement"]:#["date", "percent_positive", "percent_negative", "percent_resolved"]:#df.columns:
            #     print(colum)
            #     print(df[colum].unique())
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
                if folder_key == "lv_glb_quality_assessment":
                    print("Moving to Historical Folder")
                    shwp.move_file_to_folder(ctx, folder_information["folder_historical_id"], id)
                    print("Correctly moved to historical folder")
            except Exception as e:
                print(f"ERROR: {e}")     

        except Exception as e:
            print(e)


def main(optional: list):
    
    match optional[0]:
        case 1:
            # Getting Configs
            folder_key = "lv_glb_percent_on_queve"
            folder_information = configs[folder_key]["folder_information"]
            save_information = configs[folder_key]["save_information"]
            read_information = configs[folder_key]["read_information"]
            transform_function =  configs[folder_key]["transform_function"]
            info_transform_function = configs[folder_key]["info_transform_function"]
        case 2:
            # Getting Configs
            folder_key = "lv_glb_quality_assessment"
            folder_information = configs[folder_key]["folder_information"]
            save_information = configs[folder_key]["save_information"]
            read_information = configs[folder_key]["read_information"]
            transform_function =  configs[folder_key]["transform_function"]
            info_transform_function = configs[folder_key]["info_transform_function"]
        case 3:
            # Getting Configs
            folder_key = "lv_glb_service_level_requirement"
            folder_information = configs[folder_key]["folder_information"]
            save_information = configs[folder_key]["save_information"]
            read_information = configs[folder_key]["read_information"]
            transform_function =  configs[folder_key]["transform_function"]
            info_transform_function = configs[folder_key]["info_transform_function"]
        case 4:
            # Getting Configs
            folder_key = "lv_glb_client_report"
            folder_information = configs[folder_key]["folder_information"]
            save_information = configs[folder_key]["save_information"]
            read_information = configs[folder_key]["read_information"]
            transform_function =  configs[folder_key]["transform_function"]
            info_transform_function = configs[folder_key]["info_transform_function"]

    pipeline(folder_key, folder_information, save_information, read_information, transform_function, info_transform_function)







