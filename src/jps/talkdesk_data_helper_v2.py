import pandas as pd
import utils.dbutils as dbutils
from src.jps.talkdesk_reports_configs import reports_configs


def upload_talkdesk_data_by_halfs(report_name: str, info: str):
    config = reports_configs[report_name][info]
    schema = config["schema"]
    table_name = config["table_name"]
    delete_keys = config["delete_keys"]
    file_name = f"src\jps\last_{report_name}_{info}_data_to_upload.csv"
    file_name = "src\jps\ivr_studio_sept_to_load.csv"
    df = pd.read_csv(file_name)
    df["started_at_utc"] = pd.to_datetime(df.started_at_utc)
    
    dates = set(pd.to_datetime(df.started_at_utc).dt.date)
    for date in sorted(dates):
        test_df = df[df.started_at_utc.dt.date == date].copy()
        print(test_df)
        conn = dbutils.open_connection_with_scripting_account()
        try:
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, test_df, schema, table_name)
        except Exception as e:
            print(e)
    
    
    
    

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