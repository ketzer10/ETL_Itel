import src.anyone_home.central.helpers as helpers
import src.anyone_home.central.config as config
import utils.dbutils as dbutils
import utils.dfutils as dfutils
import utils.utils as utils
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd

def downloader(download_days: int, shop_type: str):
    date_list = [(dt.today() - timedelta(days=x)).strftime("%m/%d/%Y") for x in range(download_days)]
    date_list.reverse()

    credentials = utils.get_decrypted_credential(["decryption_key"], "anyone_home_central_hector")

    print(f"Downloading data from {date_list[0]} to {date_list[len(date_list)-1]} for {shop_type}")
    
    print("Logging into central website.")
    my_cookie = helpers.get_session_cookies(credentials["username"], credentials["password"])

    print("Getting main table data.")
    df_main_table = helpers.get_main_table_data(my_cookie, date_list[0], date_list[len(date_list)-1], shop_type)

    print("Getting card details.")
    card_details = helpers.get_all_card_info(my_cookie, df_main_table, shop_type)

    print("Consolidating dataframes.")
    df_consolidated = pd.merge(df_main_table, card_details, on="shop_sfid", how="left")
    df_consolidated["shop_completed_date"] = pd.to_datetime(df_consolidated["shop_completed_datetime"], errors="coerce").dt.date
    df_consolidated = dfutils.fill_dataframe_nulls(df_consolidated)


    table_name = config.general_params[shop_type]["table_name"]
    schema = config.general_params[shop_type]["schema"]

    # Upload to database
    conn = dbutils.open_connection_with_scripting_account()
    dbutils.perform_safe_delete_insert_with_keys(conn, ["shop_sfid"], df_consolidated, schema, table_name)



def main(optional):
    download_days = 5
    match optional[0]:
        # Maintenance
        case 1:
            shop_type = "maintenance"
            downloader(download_days, shop_type)
        
        # Audit/Leasing
        case 2:
            shop_type = "audit_leasing"
            downloader(download_days, shop_type)
