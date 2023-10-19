import utils.dbutils as dbutils
import utils.sharepoint_wrapper as shwp
from utils.utils import get_config
from utils.dfutils_automate import data_cleaner
import numpy as np
import pandas as pd

def pipeline_default_file(file_key, transform_function):
    """Truncates and uploads a forecast live Excel files to the database. 
    Args:
        sheet_name (str): The name of the sheet on the file to be uploaded.  
        table_name (str): The name of the table to upload to. 
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        file_id (str): ID for the file in sharepoint
    """
    sh_config = get_config("dshub_sharepoint_config")['files'][file_key]

    file_id = sh_config['id']
    sheet_name = sh_config['sheet_name']
    schema = sh_config['schema']
    table_name = sh_config['target_table']

    print(f"Running script for {schema}.{table_name} from {sheet_name}")
    


    # Get Data Science Hub SharePoint context
    print("Getting SharePoint context.")
    ctx = shwp.get_datascience_hub_ctx()

    print("Opening database connection.") 
    conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database

    print("Getting file from SharePoint site.")    
    file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint

    print("Loading Excel file into pandas DataFrame.")
    df = pd.read_excel(file_obj["contents"], sheet_name=sheet_name, dtype = 'str') # Read into a DataFrame

    # Transform
    try:
      df = transform_function(df)
    except Exception as e:
        raise Exception(f"Error While Execute Transform Function. {e}")
    
    # La DB no interpreta bien los NAN, por eso los cambiamos por None       
    df = df.fillna(np.nan).replace([np.nan], [None])
    print(df)
    
    
    # Load
    print("Truncating database and reinserting.")
    # Truncate and insert into the database
    dbutils.perform_safe_truncate_insert(df, conn, schema, table_name)