import pandas as pd
import utils.dfutils as dfutils
import utils.dbutils as dbutils

def upload_reason_mappings():
    filename = r"C:\Users\StivenCabrera\Documents\etl\src\hrplus_sftp\reason_mappings.csv"
    df = pd.read_csv(filename)
    df = dfutils.fill_dataframe_nulls(df)
    print(df)
    print("Opening connection with scripting account...")
    conn = dbutils.open_connection_with_scripting_account()
    dbutils.perform_safe_truncate_insert(df, conn, schema="hrplus", target_table_name="reason_code_desc_mappings")

def main(optional: list):
    """ Runs the upload_reason_mappings
    Args:
        optional (int): Run mode.
    """

    match optional[0]:
        case 1:
            upload_reason_mappings()