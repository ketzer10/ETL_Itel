import pandas as pd
import utils.dbutils as dbutils
from src.jps.talkdesk_reports_configs import reports_configs


def upload_talkdesk_data_by_halfs(report_name: str, info: str):
    config = reports_configs[report_name][info]
    schema = config["schema"]
    table_name = config["table_name"]
    delete_keys = config["delete_keys"]
    file_name = f"src\jps\last_{report_name}_{info}_data_to_upload.csv"
    df = pd.read_csv(file_name)

    half = len(df.interaction_id.unique()) // 2

    first_half_ids = df.interaction_id.unique()[:half]
    first_half_df = df[df.interaction_id.isin(first_half_ids)]

    second_half_ids = df.interaction_id.unique()[half:]
    second_half_df = df[df.interaction_id.isin(second_half_ids)]

    print(f"Openning db connection with the scripting account...")
    conn = dbutils.open_connection_with_scripting_account()
    print(f"Uploading first half df...")
    print(first_half_df)
    dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, first_half_df, schema, table_name)
    
    print(f"Openning db connection with the scripting account...")
    conn = dbutils.open_connection_with_scripting_account()
    print(f"Uploading second half df...")
    print(second_half_df)
    dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, second_half_df, schema, table_name)

def main(optional: list):
    """Runs the upload_talkdesk_data_by_halfs

    Args:
        optional (list): _description_
    """
    
    match optional[0]:
        case 1:
            report_name = "studio_flow_execution"
            info = "ivr"
            upload_talkdesk_data_by_halfs(report_name, info)