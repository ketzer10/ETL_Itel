""" 
Downloads an Excel file containing commits accepts from the SharePoint and uploads to the database.  
"""

from numpy import mat
import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils

def sheet_downloader_and_uploader(sheet_name: str, table_name: str, expected_columns: list, schema: str, file_id: str):
    """Truncates and uploads an approved overages live Excel files to the database. 
    Args:
        sheet_name (str): The name of the sheet on the file to be uploaded.  
        table_name (str): The name of the table to upload to. 
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        file_id (str): ID for the file in sharepoint
    """
    print('Getting SharePoint context.')
    ctx = shwp.get_datascience_hub_ctx()
    print('Opening database connection.') # Get Data Science Hub SharePoint context
    conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
    print('Getting file from SharePoint site.')    
    file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
    print('Loading Excel file into pandas DataFrame.')
    df = pd.read_excel(file_obj['contents'], sheet_name=sheet_name) # Read into a DataFrame

    # Verify that expected columns match the actual dataframe columns
    assert expected_columns == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'

    print('Truncating database and reinserting.')
    # Truncate and insert into the database
    dbutils.perform_safe_truncate_insert(df, conn, schema, table_name)

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """

    match optional [0]:
        case 1:
            sheet_name = 'MBL_CARE'
            table_name = 'glb_mobile_care_commits'
            expected_columns = ['half_hour_interval', 'committed_hours']
            schema = 'altice'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['altice_committed_hours']['id']
            sheet_downloader_and_uploader(sheet_name, table_name, expected_columns, schema, file_id)
        
        case 2:
            sheet_name = 'MBL_RETENTION'
            table_name = 'glb_mobile_retention_commits'
            expected_columns = ['half_hour_interval', 'committed_hours']
            schema = 'altice'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['altice_committed_hours']['id']
            sheet_downloader_and_uploader(sheet_name, table_name, expected_columns, schema, file_id)
        
        case 3:
            sheet_name = 'SDL'
            table_name = 'glb_sdl_commits'
            expected_columns = ['half_hour_interval', 'committed_hours']
            schema = 'altice'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['altice_committed_hours']['id']
            sheet_downloader_and_uploader(sheet_name, table_name, expected_columns, schema, file_id)
        
        case 4:
            sheet_name = 'OPT'
            table_name = 'glb_opt_commits'
            expected_columns = ['half_hour_interval', 'committed_hours']
            schema = 'altice'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['altice_committed_hours']['id']
            sheet_downloader_and_uploader(sheet_name, table_name, expected_columns, schema, file_id)

        case 5: 
            sheet_name = 'GLB'
            table_name = 'glb_commits'
            expected_columns = ['half_hour_interval', 'lob', 'committed_hours']
            schema = 'altice'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['altice_committed_hours']['id']
            sheet_downloader_and_uploader(sheet_name, table_name, expected_columns, schema, file_id)            