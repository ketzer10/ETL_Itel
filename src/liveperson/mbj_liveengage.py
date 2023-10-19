""" 
Downloads an Excel file containing productivity data from the SharePoint, uploads to the database and moves to archived.
"""

import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
import numpy as np

def transformations(df, expected_columns, report):    
    df.columns = expected_columns
    match(report):
        case 0:
            df['first_response_time_agent_assignment'] = df['first_response_time_agent_assignment'].astype(str)
            df['first_response_time_agent_assignment'] = df['first_response_time_agent_assignment'].astype('datetime64[ns]')
            df['first_response_time_agent_assignment'] = df['first_response_time_agent_assignment'].dt.second + (df['first_response_time_agent_assignment'].dt.minute*60)+ (df['first_response_time_agent_assignment'].dt.hour*3600)

            df['avg_response_time_agent'] = df['avg_response_time_agent'].astype(str)
            df['avg_response_time_agent'].replace('None', '00:00:00', inplace=True)
            df['avg_response_time_agent'] = df['avg_response_time_agent'].astype('datetime64[ns]')
            df['avg_response_time_agent'] = df['avg_response_time_agent'].dt.second + (df['avg_response_time_agent'].dt.minute*60)+ (df['avg_response_time_agent'].dt.hour*3600)
            df['avg_response_time_agent'].replace(0, np.nan, inplace=True)

            df['avg_segment_duration'] = df['avg_segment_duration'].astype(str)
            df['avg_segment_duration'].replace('None', '00:00:00', inplace=True)
            df['avg_segment_duration'] = df['avg_segment_duration'].astype('datetime64[ns]')
            df['avg_segment_duration'] = df['avg_segment_duration'].dt.second + (df['avg_segment_duration'].dt.minute*60)+ (df['avg_segment_duration'].dt.hour*3600)
            df['avg_segment_duration'].replace(0, np.nan, inplace=True)

        case 1:
            df['online_sec'] = df['online_sec'].astype(str)
            df['online_sec'] = df['online_sec'].astype('datetime64[ns]')
            df['online_sec'] = df['online_sec'].dt.second + (df['online_sec'].dt.minute*60)+ (df['online_sec'].dt.hour*3600)

            df['away_sec'] = df['away_sec'].astype(str)
            df['away_sec'] = df['away_sec'].astype('datetime64[ns]')
            df['away_sec'] = df['away_sec'].dt.second + (df['away_sec'].dt.minute*60)+ (df['away_sec'].dt.hour*3600)
            df['away_sec'].replace(0, np.nan, inplace=True)

            df['login_sec'] = df['login_sec'].astype(str)
            df['login_sec'] = df['login_sec'].astype('datetime64[ns]')
            df['login_sec'] = df['login_sec'].dt.second + (df['login_sec'].dt.minute*60)+ (df['login_sec'].dt.hour*3600)
            df['login_sec'].replace(0, np.nan, inplace=True)

            df['status_desc'].fillna(df['status'], inplace=True)

    df = dfutils.fill_dataframe_nulls(df)

    return df

def sheet_downloader_and_uploader(expected_columns: list, folder_key: str, schema: str, table_name: str, report: int):
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
            df = pd.read_excel(file_obj['contents'], skiprows = 2) # Read into a DataFrame

            # Transform dataframe
            df = transformations(df, expected_columns, report)            

            # Verify that expected columns match the actual dataframe columns
            assert expected_columns == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'     

            dbutils.perform_safe_delete_insert_with_keys(conn, ['date', 'agent_id'], df, schema, table_name)

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
    schema = 'liveperson'

    match(optional[0]):
        case 1:
            folder_key = 'liveperson_mbj_chat_data'
            table_name = 'mbj_chat_data'       
            expected_columns = ['date','agent_name','agent_id','agent_email','skill','interactive_conversations',
                                'ccplh','handled_conversation','closed_conversation','agent_load','first_response_time_agent_assignment',
                                'avg_response_time_agent','avg_segment_duration','transfers_to_skill','transfers_to_queue','close_rate',
                                'rcr_1_hour','rcr_1_day','rcr_3_day','rcr_7_day','mcs','csat_unified','agent_responses','avg_customer_responses',
                                'agent_segments','consumer_responses']    
            report = 0        
        case 2:
            folder_key = 'liveperson_mbj_agent_prod'
            table_name = 'mbj_agent_productivity'
            expected_columns = ['date','agent_name','agent_id','agent_email','interval','status','status_desc',
                                'skill','online_sec','away_sec','login_sec']
            report = 1    
        
    sheet_downloader_and_uploader(expected_columns, folder_key, schema, table_name, report)