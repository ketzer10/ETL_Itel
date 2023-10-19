import utils.utils as utils
import utils.dbutils as dbutils
import utils.dfutils as dfutils
import src.database_movers.hrmaster.configs as hrm_configs
import pandas as pd

def download_data(query: str, params: list) -> pd.DataFrame:
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
            # glb_external_qa_audit_leasing
            # Get the data and parameters
            case_config = config_dict["glb_external_qa_audit_leasing"]
            data = download_data(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            # Perform the upload
            dbutils.perform_safe_truncate_insert(data, conn, dst_schema, dst_table)
        case 2:
            # glb_external_qa_maintenance
            # Get the data and parameters
            case_config = config_dict["glb_external_qa_maintenance"]
            data = download_data(case_config["query"], case_config["params"])
            dst_schema = case_config["destination_schema"]
            dst_table = case_config["destination_table"]
            # Perform the upload
            dbutils.perform_safe_truncate_insert(data, conn, dst_schema, dst_table)
