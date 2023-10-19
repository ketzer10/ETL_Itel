import utils.utils as utils
import utils.dbutils as dbutils
import utils.dfutils as dfutils
import src.database_movers.hrm.configs as hrm_configs
import pandas as pd

def download_from_hrm(query: str, params: list) -> pd.DataFrame:
    """Downloads data from HRM MBJSQL UHRDB database and loads it into a Pandas dataframe. Needs to be connected
    to itel corporate network to download the data since the database doesn't have a public IP address. 

    Args:
        query (str): The SQL query used to download the data. This query must output the data in the same format to be
        used in the destination database.
        params (list): The parameters to be passed to the SQL query.
    Returns:
        pd.DataFrame: The Pandas Dataframe with the result of the query.
    """
    db_config = utils.get_config("database_configs")["sql_server_mbjhrm"]

    hostname = db_config["hostname"]
    database_name = db_config["database_name"]

    credentials = utils.get_decrypted_credential(["decryption_key"], "mbj_sql_server_eduardo")
    username = credentials["username"]
    password = credentials["password"]

    print("Opening connection with HRM SQL Server.")
    conn = dbutils.open_connection(hostname, database_name, username, password)

    print("Reading HRM data into pandas dataframe.")
    df = pd.read_sql_query(query, conn, params=params)    
    df = dfutils.fill_dataframe_nulls(df)
    conn.close()
    return df

def main(optional = None):
    # Get the config dictionary
    config_dict = hrm_configs.configs

    # Open the connection to the database. Same connection will be reused in all cases.
    conn = dbutils.open_connection_with_scripting_account()

    match optional[0]:
        case 1:
            # Get the data and parameters
            case_config = config_dict["hrm_attendance"]
            data = download_from_hrm(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["date"]

            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table)
        case 2:
            # Get the data and parameters
            case_config = config_dict["hrm_employees"]
            data = download_from_hrm(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]

            # Perform the upload
            dbutils.perform_safe_truncate_insert(data, conn, dst_schema, dst_table)
        case 3:
            # Get the data and parameters
            case_config = config_dict["hrm_departments"]
            data = download_from_hrm(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]

            # Perform the upload
            dbutils.perform_safe_truncate_insert(data, conn, dst_schema, dst_table)
        case 4:
            # Get the data and parameters
            case_config = config_dict["hrm_jobs"]
            data = download_from_hrm(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]

            # Perform the upload
            dbutils.perform_safe_truncate_insert(data, conn, dst_schema, dst_table)
        case 5:
            # Get the data and parameters
            case_config = config_dict["hrm_schedule_day_types"]
            data = download_from_hrm(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]

            # Perform the upload
            dbutils.perform_safe_truncate_insert(data, conn, dst_schema, dst_table)
        case 6:
            # Get the data and parameters
            case_config = config_dict["hrm_attendance_codes"]
            data = download_from_hrm(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]

            # Perform the upload
            dbutils.perform_safe_truncate_insert(data, conn, dst_schema, dst_table)
        case 7:
            # Get the data and parameters
            case_config = config_dict["hrm_attendance_details"]
            data = download_from_hrm(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["date"]

            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table)
        case 8:
            # Get the data and parameters
            case_config = config_dict["hrm_attendance_summary"]
            data = download_from_hrm(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["date"]

            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table)
        case 9:
            # Get the data and parameters
            case_config = config_dict["hrm_schedules"]
            data = download_from_hrm(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["schedule_date"]

            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table)