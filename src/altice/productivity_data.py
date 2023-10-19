"""
Downloads an Client Reports with productivity data for Altice KGN, MBJ and SLU.
The argument passed to main determines which site will get updated.
"""
import utils.utils as utils
import utils.sharepoint_wrapper  as shwp
import pandas as pd
import utils.dbutils as dbutils
import numpy as np
import src.altice.reports_configs as rconfig
from pyxlsb import open_workbook as open_xlsb, convert_date

def transformation(df: pd.DataFrame)->pd.DataFrame:
    # transform before df_handling
    df["thirty_day_repeat_pct"] = np.nan
    df["repeat_thirty_days"] = np.nan
    df["repeat_forty_day"] = np.nan

    #df_handling
    df = df[rconfig.altice_productivity["final_columns_order"]]
    df.columns =  rconfig.altice_productivity["headers"] 
    
    # transform affter df_handling manage dates for xlsb
    df.dropna(subset = ['agent_id'], inplace = True) 
    df[['date','last_call_date']] = df[['date','last_call_date']].astype('datetime64[ns]')
    df['agent_id'] = df['agent_id'].str.strip().str.upper()
    df = df.fillna(np.nan).replace([np.nan], [None])

    # for column in rconfig.altice_productivity["date_columns"]:
    #     df[column] = df[column].replace([" ", "-", "nan", "TBD"], [np.nan, np.nan, np.nan, np.nan])
    #     df[column] = df[column].fillna(0)
    #     df[column] = df[column].astype("int")
    #     df[column] = df[column].replace([0], [" "])
    #     df[column] = df[column].apply(lambda date: convert_date(date))


    return df

def main(optional: list):
    """ Runs the productivity data for KGN [1], MBJ [2] or SLU [3].

    Args:
        optional (int): Run mode. KGN [1], MBJ [2] or SLU [3].
    """

    print('Getting SharePoint context.')
    sh_configs = utils.get_config('dshub_sharepoint_config')                                                            
    ctx = shwp.get_datascience_hub_ctx()                                                                               
    
    match optional[0]:
        # Getting the right id based on the optional argument passed.
        case 1:
            folder_key = 'altice_kgn_daily_prod'
            keys = ['agent_id','date','csr_tsr','comm_resi','product_brand']
        case 2:
            folder_key = 'altice_mbj_daily_prod'
            keys = ['agent_id','date','csr_tsr','comm_resi','product_brand']
        case 3:
            folder_key = 'altice_slu_daily_prod'
            keys = ['agent_id','date','csr_tsr','comm_resi','product_brand']
    
    # Processing of the files in each folder
    print(f"Running script for {folder_key}")
    folder_id = sh_configs['folders'][folder_key]["id"]
    file_ids = shwp.get_files_by_folder_id(ctx, folder_id = folder_id)
    
    # Constant variables
    SCHEMA = 'altice' 
    TARGET_TABLE = sh_configs['folders'][folder_key]["target_table"]                                                    
    
    for id in file_ids:
        print("Accessing File with id: ", id)
        print('Downloading file')
        try: 
            # Extraction Phase
            io_data = shwp.get_sharepoint_file_by_id(ctx, id)
            print(io_data['file_name'])
            print("Data succesfully downloaded \nReading into dataframe")
            df = pd.read_excel(io_data["contents"], sheet_name = "data")#, engine = "pyxlsb")

            # Transforming dataframe
            df = transformation(df)

            # Creating Database connection
            print("Opening connection to database")
            conn = dbutils.open_connection_with_scripting_account()
            cursor = conn.cursor()
            cursor.fast_executemany = True
                    
            # Loading Phase
            try:
                stm = dbutils.generate_dataframe_upsert_stmt(keys = keys, source_df = df, target_table_name = SCHEMA+'.'+TARGET_TABLE)
                print(f'Importing to {SCHEMA}.{TARGET_TABLE}')
                cursor.executemany(stm['stmt'], stm['params'])
                cursor.commit()
                print("New Data Commited")
                
                # Moving to Historical Folder
                print("Moving to Historical Folder")
                shwp.move_file_to_folder(ctx, sh_configs['folders'][folder_key]['historical_id'], id)
                print("Correctly moved to historical folder")
            except Exception as e:
                print(f"ERROR: {e}") 
            
        except Exception as e:
            print("Error Downloading data \n Details: ",e)
        pass
    
  
            
