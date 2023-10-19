""" 
Reads an Excel file containing Adherence from the SharePoint and uploads to the database.
This solution is temporary since we have a scraper. A database mover would require less input as well. 
"""

import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
import datetime
from io import StringIO

def sheet_downloader_and_uploader(table_name: str, expected_columns: list, schema: str, file_id: str, sheet_name: str = None):
    """Truncates and uploads a forecast live Excel files to the database. 
    Args:
        table_name (str): The name of the table to upload to. 
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        file_id (str): ID for the file in sharepoint
        sheet_name (str): Optional argument that specifies the sheet name. Only one sheet name can be passed. If no argument 
        is passed, the first sheet of the Excel workbook is read.
    """

    print('Getting SharePoint context.')
    ctx = shwp.get_datascience_hub_ctx()
    print('Opening database connection.') # Get Data Science Hub SharePoint context
    conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
    print('Getting file from SharePoint site.')    
    file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
    print('Loading Excel file into pandas DataFrame.')
    
    # If no sheet name was passed, just read the first tab of the sheet. Otherwise read the passed name
    if sheet_name is None:
        df = pd.read_excel(file_obj['contents']) # Read into a DataFrame
    else:
        df = pd.read_excel(file_obj['contents'], sheet_name=sheet_name) # Read into a DataFrame

    # Verify that expected columns match the actual dataframe columns
    assert expected_columns == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'

    # Fill empty values with NULLs
    df = dfutils.fill_dataframe_nulls(df)    

    print('Truncating database and reinserting.')
    # Truncate and insert into the database
    dbutils.perform_safe_truncate_insert(df, conn, schema, table_name)

    latest_date = df['date'].max()

    if(latest_date >=  pd.Timestamp(datetime.date.today() - datetime.timedelta(days=1))):
        try: 
            output_str = datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S')
            file_buffer = StringIO(output_str)    
            file_buffer.seek(0)
            text_file = file_buffer.getvalue().encode('utf-8')    

            filename = f"AOH ADH i54 ran on {output_str}.txt"

            shwp.upload_file_to_sharepoint_folder(ctx, "c3b1929e-1707-46aa-ae8c-ca5dae5bc5c6", filename, text_file)
        except: 
            pass # Should not prevent etl script execution from updating if this fails

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """

    sheet_name = 'Azure_Adherence'
    table_name = 'glb_adherence'
    expected_columns = ['transactions', 'scheduled_in_queue', 'actual_in_queue', 'in_queue_variance', 'scheduled_out_queue', 'actual_out_queue', 'out_queue_variance', 'total_scheduled', 'total_variance', 'name', 'location', 'date']
    schema = 'anyone_home'
    file_id = utils.get_config('dshub_sharepoint_config')['files']['anyone_home_adherence']['id']
    file_name = utils.get_config('dshub_sharepoint_config')['files']['anyone_home_adherence']['name']

    print(f'Uploading {file_name}')
    sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)

