""" 
Downloads an Excel file containing NRRC from the SharePoint, uploads to the database and moves to archived.
"""

import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils

def transformations(df, expected_columns):    
    df.columns = expected_columns
    df.dropna(subset=['ps_id'],inplace=True)  
    df['date'] = df['date'].astype('datetime64[ns]')
    df['half_hour_interval'] = df['half_hour_interval'].astype('datetime64[ns]')
    df['half_hour_interval'] = pd.to_datetime(df['half_hour_interval'], errors='coerce', format ="%Y-%m-%d %H:%M:%S")      
        
    df['not_ready_sec'] = df['not_ready_sec'].astype('datetime64[ns]')
    df['not_ready_sec'] = df['not_ready_sec'].dt.second + df['not_ready_sec'].dt.minute * 60 + df['not_ready_sec'].dt.hour * 3600

    df['not_ready_pct'] = pd.to_numeric(df.not_ready_pct.str.replace('%',''))
    df['not_ready_reason_pct_duration'] = pd.to_numeric(df.not_ready_reason_pct_duration.str.replace('%',''))

    code_agent_name = df['agent_name'].str.split('.', 1, expand=True)
    df['agent_name'] = code_agent_name[1].str.split('_').str.join(' ')
    
    df = dfutils.fill_dataframe_nulls(df)

    return df

def sheet_downloader_separator_and_uploader(expected_columns: list, folder_key: str, schema: str):
    """
    Reads all productivity Excel files in the folder and deletes and uploads to the database. 
    Args:                
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        folder_key (str): Name of the key of the folder in sharepoint.
    """
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

            file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
            print('Loading Excel file into pandas DataFrame.')
            df = pd.read_csv(file_obj['contents'], dtype=object) # Read into a DataFrame

            # Transform dataframe
            df = transformations(df, expected_columns)    

            df.head()        

            # Verify that expected columns match the actual dataframe columns
            assert expected_columns == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'   

            df_opt = df[df.organization.str.contains('OPT')]
            table_name_opt = 'glb_optimum_nrrc'        
            df_mob = df[df.organization.str.contains('MOB')]
            table_name_mob = 'glb_mobile_nrrc'
            df_sdl = df[df.organization.str.contains('SDL')]
            table_name_sdl = 'glb_suddenlink_nrrc'

            print(df_opt.size)
            print(df_mob.size)
            print(df_sdl.size)

            if(df_opt.size > 0):
                print('Opening database connection.') # Get Data Science Hub SharePoint context
                conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
                cursor = conn.cursor()                                                                                   
                cursor.fast_executemany = True                   
                dbutils.perform_safe_delete_insert_with_keys(conn, ['date'], df_opt, schema, table_name_opt)

            if(df_mob.size > 0):
                print('Opening database connection.') # Get Data Science Hub SharePoint context
                conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
                cursor = conn.cursor()                                                                                   
                cursor.fast_executemany = True  
                conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database           
                dbutils.perform_safe_delete_insert_with_keys(conn, ['date'], df_mob, schema, table_name_mob)

            if(df_sdl.size > 0):
                print('Opening database connection.') # Get Data Science Hub SharePoint context
                conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
                cursor = conn.cursor()                                                                                   
                cursor.fast_executemany = True  
                conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database           
                dbutils.perform_safe_delete_insert_with_keys(conn, ['date'], df_sdl, schema, table_name_sdl)

            # Moving to Historical Folder
            print("Moving to Historical Folder")
            shwp.move_file_to_folder(ctx, historical_folder_id, file_id)
            print("Correctly moved to historical folder")                       

        except Exception as e:
            conn.rollback()
            print('Table not uploaded, rolling back to previous state \n Error Details: ', e)
        pass 

def sheet_downloader_and_uploader(expected_columns: list, folder_key: str, schema: str, table_name: str):
    """
    Reads all productivity Excel files in the folder and deletes and uploads to the database. 
    Args:        
        table_name (str): The name of the table to upload to. 
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        folder_key (str): Name of the key of the folder in sharepoint.
    """
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
            print('Loading Excel file into pandas DataFrame.')
            df = pd.read_csv(file_obj['contents'], dtype=object) # Read into a DataFrame

            # Transform dataframe
            df = transformations(df, expected_columns)                  

            # Verify that expected columns match the actual dataframe columns
            assert expected_columns == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'           
            
            dbutils.perform_safe_delete_insert_with_keys(conn, ['date'], df, schema, table_name)

            # Moving to Historical Folder
            print("Moving to Historical Folder")
            shwp.move_file_to_folder(ctx, historical_folder_id, file_id)
            print("Correctly moved to historical folder")                       

        except Exception as e:
            conn.rollback()
            print('Table not uploaded, rolling back to previous state \n Error Details: ', e)
        pass 

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """    
    schema = 'altice'
    expected_columns = ['organization','location','department','skill','language','agent_name','ps_id','date',
                        'half_hour_interval','not_ready_sec','not_ready_pct','not_ready_reason_code','not_ready_reason_count',
                        'not_ready_reason_duration','not_ready_reason_pct_duration',
]

    match(optional[0]):
        case 1:
            folder_key = 'altice_suddenlink_nrrc_eod'
            table_name = 'glb_suddenlink_nrrc'
            sheet_downloader_and_uploader(expected_columns, folder_key, schema, table_name)
        case 2:
            folder_key = 'altice_optimum_mobile_nrrc_eod'            
            sheet_downloader_separator_and_uploader(expected_columns, folder_key, schema)
        case 3:
            folder_key = 'altice_suddenlink_nrrc_eod'            
            sheet_downloader_separator_and_uploader(expected_columns, folder_key, schema)
