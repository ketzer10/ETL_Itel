import utils.utils as utils
import utils.dbutils as dbutils
import utils.dfutils as dfutils
import src.office_depot.database_mover.configs as hrm_configs
import pandas as pd

def download_data(query: str, params: list, first_time = False) -> pd.DataFrame:
    """Downloads data from GCP PostgreSQL database and loads it into a Pandas dataframe.

    Args:
        query (str): The SQL query used to download the data. This query must output the data in the same format to be
        used in the destination database.
        params (list): The parameters to be passed to the SQL query.
    Returns:
        pd.DataFrame: The Pandas Dataframe with the result of the query.
    """
    db_config = utils.get_config("database_configs")["postgresql_gcp"]

    hostname = db_config["hostname"]
    database_name = db_config["database_name"]

    credentials = utils.get_decrypted_credential(["decryption_key"], "postgre_sql_eduardo")
    username = credentials["username"]
    password = credentials["password"]

    print("Opening connection with GCP PostgreSQL server.")
    conn = dbutils.open_postgresql_connection(hostname, database_name, username, password)

    print("Reading GCP data into pandas dataframe.")
    if first_time == True:
        df = pd.read_sql_query(query, conn)  
    else:    
        df = pd.read_sql_query(query, conn, params = params)    
    df = dfutils.fill_dataframe_nulls(df)
    conn.close()
    return df

def reverse_download_data(query: str, params: list, first_time = False) -> pd.DataFrame:
    """Downloads data from MSSQL  database and loads it into a Pandas dataframe.

    Args:
        query (str): The SQL query used to download the data. This query must output the data in the same format to be
        used in the destination database.
        params (list): The parameters to be passed to the SQL query.
    Returns:
        pd.DataFrame: The Pandas Dataframe with the result of the query.
    """

    print("Opening connection with MSSQL Scripting Account.")
    conn = dbutils.open_connection_with_scripting_account()

    print("Reading MSSQL data into pandas dataframe.")
    if first_time == True:
        df = pd.read_sql_query(query, conn)  
    else:    
        df = pd.read_sql_query(query, conn, params = params)    
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
            case_config = config_dict["od_geo_agent_activity_team_time"]
            data = download_data(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["thedate"]
            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table)
        case 2: 
            # Get the data and parameters
            case_config = config_dict["od_wah_agent_activity_team_time"]
            data = download_data(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["thedate"]
            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table)            
        case 3: 
            # Get the data and parameters
            case_config = config_dict["od_geo_journey_agent_summary"]
            data = download_data(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["date"]
            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table)   
        case 4: 
            # Get the data and parameters
            case_config = config_dict["od_wah_journey_agent_summary"]
            data = download_data(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["date"]
            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table)
        case 5: 
            # Get the data and parameters
            case_config = config_dict["od_glb_journey_calls_handled_by_queue_team"]
            data = download_data(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["thedate"]
            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table) 
        case 6: 
            # Get the data and parameters
            case_config = config_dict["od_geo_crm_daily_chat_phone"]
            data = download_data(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["date"]
            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table)    
        case 7: 
            # Get the data and parameters
            case_config = config_dict["od_wah_crm_daily_phone"]
            data = download_data(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["date"]
            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table)  
        case 8: 
            # Get the data and parameters
            case_config = config_dict["od_geo_chat_activity_oracle"]
            data = download_data(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["date", "agent_name"]
            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table) 
        case 9: 
            # Get the data and parameters
            case_config = config_dict["od_geo_agent_activity_by_channel"]
            data = download_data(case_config["query"], case_config["params"], first_time = False)
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["date", "office_depot_id"]
            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table)
        case 10: 
            # Get the data and parameters
            case_config = config_dict["od_wah_agent_activity_by_channel"]
            data = download_data(case_config["query"], case_config["params"], first_time = False)
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["date", "office_depot_id"]
            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table)
        case 11: 
            # Get the data and parameters
            case_config = config_dict["od_internal_qa"]
            data = download_data(case_config["query"], case_config["params"], first_time = True)
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["date", "sessionid"]
            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, data, dst_schema, dst_table)                                                 
        case 12: 
            # Get the data and parameters
            case_config = config_dict["od_reverse_calls_handled"]
            data = reverse_download_data(case_config["query"], case_config["params"], first_time = False)
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["thedate"]

            db_config = utils.get_config("database_configs")["postgresql_gcp"]
            hostname = db_config["hostname"]
            database_name = db_config["database_name"]
            credentials = utils.get_decrypted_credential(["decryption_key"], "postgre_sql_eduardo")
            username = credentials["username"]
            password = credentials["password"]
            print("Opening connection with GCP PostgreSQL server.")
            pg_conn = dbutils.open_postgresql_connection(hostname, database_name, username, password)            
            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(pg_conn, delete_keys, data, dst_schema, dst_table)
        case 13: 
            # Get the data and parameters
            case_config = config_dict["od_reverse_team_time"]
            data = reverse_download_data(case_config["query"], case_config["params"], first_time = False)
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            delete_keys = ["thedate"]

            db_config = utils.get_config("database_configs")["postgresql_gcp"]
            hostname = db_config["hostname"]
            database_name = db_config["database_name"]
            credentials = utils.get_decrypted_credential(["decryption_key"], "postgre_sql_eduardo")
            username = credentials["username"]
            password = credentials["password"]
            print("Opening connection with GCP PostgreSQL server.")
            pg_conn = dbutils.open_postgresql_connection(hostname, database_name, username, password)            
            # Perform the upload
            dbutils.perform_safe_delete_insert_with_keys(pg_conn, delete_keys, data, dst_schema, dst_table)            
            