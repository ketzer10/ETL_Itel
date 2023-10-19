from asyncio.windows_events import NULL
import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
from src.scheduling.config.config_files import configs
import src.scheduling.functions.schedules_functions as sched_fns
import numpy as np
from src.scheduling.functions.load_functions import sftp
import os
pd.options.mode.chained_assignment = None


sh_config = utils.get_config("dshub_sharepoint_config")

print("Getting SharePoint context")
ctx = shwp.get_datascience_hub_ctx()


def sheet_downloader_and_uploader(FOLDER_ID: str, file_type: str, FOLDER_KEY: str, read_with_dtype: dict, client: str, site: str, site_filter = 0, skiprows = 0, sheet_name = 0):

    lob = client+site
    print("Loading schedules for", lob)
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id = FOLDER_ID)
    files_read = []
    file_max_date = []
    file_min_date = []
    file_indices = []
    successful_file_ids = []
    file_index = 0
    print("Files to process:", len(file_ids))
    for id in file_ids:        
        print("Accessing File with id: ", id)
        print('Downloading file')
        try:  
            # Extraction Phase
            io_data = shwp.get_sharepoint_file_by_id(ctx, id)
            print(io_data['file_name'])
            print("Data succesfully downloaded \nReading into dataframe")
            output_folder_id = sh_config["folders"][FOLDER_KEY]["hrplus_format_output"]
            historical_folder_id = sh_config["folders"][FOLDER_KEY]["historical_id"]

            match file_type:
                case "csv":
                    df = pd.read_csv(io_data['contents'], skiprows=skiprows, encoding= 'unicode_escape', dtype = read_with_dtype)
                case "xlsx":
                    df = pd.read_excel(io_data['contents'], skiprows=skiprows, dtype = read_with_dtype, sheet_name=sheet_name)
            print("Loaded to df", df.shape)
            print("Headers", df.columns.to_list())            
            print(df.head())

            print(site)
            if (site_filter == 1):
                df = sched_fns.site_filter(df, client, site)            
            
            # data handling phase
            df, info = configs[FOLDER_KEY]["transform_function"](df, configs[FOLDER_KEY]["info_transform_function"])

            # validation(df=df)
            print("Filling dataframe nulls.")
            df = dfutils.fill_dataframe_nulls(df, "")


            if (site_filter == 2):
                df = sched_fns.site_filter(df, client, site)            

            if(df.size>0):
                print(df.shape)
                max_date = max(df["date"].astype("datetime64").dt.strftime("%Y%m%d"))
                min_date = min(df["date"].astype("datetime64").dt.strftime("%Y%m%d"))            
                files_read.append(df)
                file_indices.append(file_index)
                file_max_date.append(max_date)
                file_min_date.append(min_date)
                successful_file_ids.append(id)
                file_index += 1                                    
            else:
                print("Empty df, unable to output file")            

            #sftp(host='20.94.92.208',username='iteluser',password='y7$$J$fmth',port=4011)
            
        except Exception as e:
            print(e)

    if len(file_ids) > 0:
        sched_fns.file_combiner(file_indices, file_min_date, file_max_date, files_read, lob, output_folder_id, successful_file_ids, historical_folder_id, ctx)
        info['date'] = pd.Timestamp.utcnow()
        info['lob'] = lob

        conn = dbutils.open_connection_with_scripting_account()

        try:
            dbutils.perform_safe_delete_insert_with_keys(
                conn = conn, 
                delete_keys = ['lob','date'], 
                source_df = info, 
                schema = 'misc', 
                target_table_name = 'glb_schedules_hrplus'
            )
        except Exception as e:
            print(f"ERROR: {e}") 
    else:
        print("No files to process")
    

def main(optional: list):
    sheet_name = 0
    site_filter = 0 # 0 = No; 1 = Provided in file, 2 = Added during processing

    match optional[0]:
        case 0:
            client = "Hilton"
            site = "SLU"            
            FOLDER_KEY = "slu_hilton_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            site_filter = 1
        case 1:
            client = "Altice"
            site = "SLU"
            FOLDER_KEY = "slu_altice_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 1 
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            site_filter = 1
        case 2:
            client = "Kroger"
            site = "SLU"
            site_filter = 0
            FOLDER_KEY = "slu_kroger_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 0 
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 3:
            client = "TDSFinancialServices"
            FOLDER_KEY = "slu_tds_financial_services_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 7 
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            site = "SLU"
            site_filter = 2
        case 4:
            client = "TDSRepair"
            FOLDER_KEY = "slu_tds_repairs_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 7 
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            site = "SLU"
            site_filter = 2
        case 5:
            client = "TDSSales"
            FOLDER_KEY = "slu_tds_sales_schedules"            
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 7 
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            site = "SLU"
            site_filter = 2
        case 6:
            client = "Ancestry"
            site = "KGN"
            site_filter = 0
            FOLDER_KEY = "kgn_ancestry_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 5 
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 7: 
            client = "1800Flowers"
            site = "MBJ"
            site_filter = 0
            FOLDER_KEY = "mbj_1800_flowers_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 8:
            client = "TDSFieldServices"
            site = "MBJ"
            site_filter = 2
            FOLDER_KEY = "mbj_tds_field_services_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 7 
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 9: 
            client = "Speedy"
            site = "SLU"
            site_filter = 0
            FOLDER_KEY = "slu_speedy_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 10: 
            client = "Speedy"
            site = "MBJ"
            site_filter = 0
            FOLDER_KEY = "mbj_speedy_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]       
        case 11: 
            client = "ActivEngage"
            site = "MBJ"
            site_filter = 0
            FOLDER_KEY = "mbj_activengage_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 1
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]  
        case 12: 
            client = "PSN"
            site = "MBJ"
            site_filter = 0
            FOLDER_KEY = "mbj_psn_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]  
        case 13: 
            client = "IAA"
            site = "KGN"
            site_filter = 0
            FOLDER_KEY = "kgn_iaa_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 14: 
            client = "Ontellus"
            site = "MBJ"
            site_filter = 0
            FOLDER_KEY = "mbj_ontellus_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]    
        case 15: 
            client = "MOH"
            site = "MBJ"
            site_filter = 0
            FOLDER_KEY = "mbj_moh_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]      
        case 16: 
            client = "Breville"
            site = "MBJ"
            site_filter = 0
            FOLDER_KEY = "mbj_breville_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 1
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 17: 
            client = "Car8"
            site = "MBJ"
            site_filter = 0
            FOLDER_KEY = "mbj_car8_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 18: 
            client = "JPS"
            site = "MBJ"
            site_filter = 0
            FOLDER_KEY = "mbj_jps_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 19: 
            client = "JPS"
            site = "KGN"
            site_filter = 0
            FOLDER_KEY = "kgn_jps_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 20: 
            client = "Kroger"
            site = "KGN"
            site_filter = 0
            FOLDER_KEY = "kgn_kroger_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 21:
            client = "Hilton"
            site = "KGN"
            site_filter = 1
            FOLDER_KEY = "kgn_hilton_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 22:
            client = "Hilton"
            site = "MBJ"
            site_filter = 1
            FOLDER_KEY = "mbj_hilton_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 23: 
            client = "TGCS"
            site = "KGN"
            site_filter = 0
            FOLDER_KEY = "kgn_tgcs_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 24: 
            client = "Lifetouch"
            site = "KGN"
            sheet_name = "LifeTouch"
            site_filter = 0
            FOLDER_KEY = "kgn_lifetouch_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 25:
            client = "TDSFinancialServices"
            FOLDER_KEY = "mbj_tds_financial_services_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 7 
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            site = "MBJ"
            site_filter = 2
        case 26:
            client = "TDSRepair"
            FOLDER_KEY = "mbj_tds_repairs_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 7 
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            site = "MBJ"
            site_filter = 2
        case 27:
            client = "TDSSales"
            FOLDER_KEY = "mbj_tds_sales_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 7 
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            site = "MBJ"
            site_filter = 2
        case 28:
            client = "Altice"
            site = "MBJ"            
            FOLDER_KEY = "mbj_altice_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 1 
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            site_filter = 1
        case 29:
            client = "Altice"
            site = "KGN"
            FOLDER_KEY = "kgn_altice_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 1 
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            site_filter = 1
        case 30:
            client = "Shutterfly"
            site = "KGN"
            sheet_name = "Shutterfly"
            FOLDER_KEY = "kgn_shutterfly_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
            site_filter = 0                                                               
        case 31: 
            client = "1800Flowers"
            site = "KGN"
            site_filter = 0
            FOLDER_KEY = "kgn_1800_flowers_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "csv"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 32: 
            client = "MIAAesthetics"
            site = "KGN"
            site_filter = 0
            FOLDER_KEY = "kgn_mia_aesthetics_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 33: 
            client = "Liveperson"
            site = "MBJ"
            site_filter = 0
            FOLDER_KEY = "mbj_liveperson_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]
        case 34: 
            client = "Walmart"
            site = "KGN"
            site_filter = 0
            FOLDER_KEY = "kgn_walmart_schedules"
            FOLDER_ID = sh_config["folders"][FOLDER_KEY]["id"]
            file_type = "xlsx"
            skiprows = 0
            read_with_dtype = configs[FOLDER_KEY]["read_with_dtype"]                            

    sheet_downloader_and_uploader(
        FOLDER_ID = FOLDER_ID, 
        file_type = file_type, 
        FOLDER_KEY = FOLDER_KEY,
        read_with_dtype=read_with_dtype,
        skiprows=skiprows,
        sheet_name=sheet_name,
        site_filter=site_filter,
        client=client,
        site=site)
