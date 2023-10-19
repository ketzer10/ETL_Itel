import pandas as pd
import utils.utils as utils
import utils.dbutils as dbutils
import utils.sharepoint_wrapper as shwp
from datetime import datetime


def elaborate_touchpoints_report():
    conn = dbutils.open_connection_with_scripting_account()
    query = """SELECT  CONVERT(date, SWITCHOFFSET(started_at_utc, '-05:00')) AS date,
       interaction_id,
       category,
       subcategory
    FROM jps.talkdesk_ivr_studio
    WHERE MONTH(CONVERT(date, SWITCHOFFSET(started_at_utc, '-05:00'))) = MONTH(GETDATE())
    AND YEAR(CONVERT(date, SWITCHOFFSET(started_at_utc, '-05:00'))) = YEAR(GETDATE())
    AND category != 'No touchpoint';"""
    
    df = pd.read_sql(query, conn)
    pivot = pd.pivot_table(df,
                           index=["category", "subcategory"],
                           columns="date",
                           aggfunc=len,
                           margins=True,
                           margins_name="Total")
    print(pivot)
    pivot.to_excel("src\jps\Touchpoints report.xlsx", index=True)
    ctx = shwp.get_datascience_hub_ctx()
    touchpoints_folder_id = utils.get_config("dshub_sharepoint_config")["folders"]["jps_touchpoints"]["id"]
    file_path = "src\jps\Touchpoints report.xlsx"
    current = datetime.now()
    # month_name = current.strftime('%B')
    max_month = df['date'].max().strftime('%B')
    file_name = f"JPS Touchpoints Report {max_month}.xlsx"
    with open(file_path, "rb") as file:
        file_bytes = file.read()
        shwp.upload_file_to_sharepoint_folder(ctx, touchpoints_folder_id, file_name, file_bytes)


def main(optional: list):
    """Runs the elaborate_touchpoints_report

    Args:
        optional (list): _description_
    """
    
    match optional[0]:
        case 1:
            elaborate_touchpoints_report()