import utils.dbutils as dbutils
import pandas as pd
import utils.utils as utils
import utils.dfutils as dfutils
import utils.sharepoint_wrapper as shwp


def sheet_downloader_and_uploader(folder_key: str):
    """
    Reads all productivity Excel files in the folder and deletes and uploads to the database. 
    Args:        
        table_name (str): The name of the table to upload to. 
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        folder_key (str): Name of the key of the folder in sharepoint.
    """

    print("Getting SharePoint context.")
    ctx = shwp.get_datascience_hub_ctx() 

    folder_id = utils.get_config('dshub_sharepoint_config')['folders'][folder_key]['id']
    historical_folder_id = utils.get_config('dshub_sharepoint_config')['folders'][folder_key]['historical_id']
    schema = utils.get_config('dshub_sharepoint_config')['folders'][folder_key]['schema']
    table_name = utils.get_config('dshub_sharepoint_config')['folders'][folder_key]['target_table']
    
    sorted_files_names_extensions_and_ids = shwp.get_files_names_extensiones_and_ids_by_folder_id(ctx, folder_id)

    file_ids = list(item[2] for item in sorted_files_names_extensions_and_ids)
    print("Files to load:", len(file_ids))

    db_config = utils.get_config("database_configs")["postgresql_gcp"]
    hostname = db_config["hostname"]
    database_name = db_config["database_name"]

    credentials = utils.get_decrypted_credential(["decryption_key"], "postgre_sql_eduardo")
    username = credentials["username"]
    password = credentials["password"]

    print("Opening connection with GCP PostgreSQL server.")
    conn = dbutils.open_postgresql_connection(hostname, database_name, username, password)

    query_mappings = 'SELECT * FROM office_depot.office_depot_mappings'
    query_employees = 'SELECT CONCAT(TRIM(first_name), \' \', TRIM(last_name)) AS full_name FROM hrmaster.hr_employee_database'

    print("Reading GCP data into pandas dataframe.")
    df_mappings = pd.read_sql_query(query_mappings, conn)
    df_employees = pd.read_sql_query(query_employees, conn)

    df_mappings = dfutils.fill_dataframe_nulls(df_mappings)
    df_employees = dfutils.fill_dataframe_nulls(df_employees)

    conn.close()

    for file_id in file_ids:
        file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
        df = pd.read_csv(file_obj['contents'], skiprows=0)
        
        df = df[["loginTime", "userId", "timeAvailable","timeAvailableForExisting","timeUnavailable"]]
        df["login_time"] = df["timeAvailable"] + df["timeAvailableForExisting"] + df["timeUnavailable"]    
        df["login_time_sec"] = (df["timeAvailable"] + df["timeAvailableForExisting"] + df["timeUnavailable"])/1000
        df["userId"] = df["userId"].str.replace("-1", "")
        df["userId"] = df["userId"].str.replace("1", "")
        df["name"] = df["userId"].str.replace("-", " ")

        df = dfutils.strip_string_columns(df, columns = ["name"])        
        df = dfutils.validate_text_columns(df, ["loginTime", "userId", "name"])
        df_mappings = dfutils.validate_text_columns(df_mappings, ["sms_username"])
        df_employees = dfutils.validate_text_columns(df_employees, ["full_name"])

        df = pd.merge(left = df, right = df_mappings, how="left", left_on="userId", right_on="sms_username")
        df = pd.merge(left = df, right = df_employees, how="left", left_on="name", right_on="full_name")

        df = df.drop_duplicates(subset=['userId', 'loginTime'])

        df = df[["loginTime", "userId", "login_time_sec", "sms_username", "full_name"]]
        df = dfutils.fill_dataframe_nulls(df, 'NaN')
        df = df[~(df["sms_username"].isnull()) | ~(df["full_name"].isnull())]

        df["date"] = df["loginTime"].str.split(expand=False).str[0]

        df = df[["date", "userId", "login_time_sec"]]
        df = dfutils.validate_date_columns(df, columns=['date'], date_format="%Y-%m-%d")

        df = df.groupby(['date', 'userId'], as_index=False).sum()

        print("Data for:", ((df['date']).min()).strftime('%Y-%m-%d'), '-',((df['date']).max()).strftime('%Y-%m-%d'))

        try:
            print('Opening database connection.') # Get Data Science Hub SharePoint context
            conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
            dbutils.perform_safe_delete_insert_with_keys(conn, ["date"], df, schema, table_name)

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
    
    folder_key = 'od_quiq_historical_stats'
        
    sheet_downloader_and_uploader(folder_key)