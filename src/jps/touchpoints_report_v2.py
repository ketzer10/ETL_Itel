import pandas as pd
import utils.utils as utils
import utils.dbutils as dbutils
import utils.sharepoint_wrapper as shwp


def elaborate_touchpoints_report():
    # Original code for pivot table
    conn = dbutils.open_connection_with_scripting_account()
    query = """SELECT CONVERT(date, SWITCHOFFSET(started_at_utc, '-05:00')) AS date,
        interaction_id,
        category,
        subcategory
        FROM jps.talkdesk_ivr_studio
        WHERE MONTH(CONVERT(date, SWITCHOFFSET(started_at_utc, '-05:00'))) = MONTH(GETDATE())
        AND YEAR(CONVERT(date, SWITCHOFFSET(started_at_utc, '-05:00'))) = YEAR(GETDATE())
        AND category != 'No touchpoint';"""

    df = pd.read_sql(query, conn)
    pivot_all = pd.pivot_table(df,
                            index=["category", "subcategory"],
                            columns="date",
                            aggfunc=len,
                            margins=True,
                            margins_name="Total")

    # Create a new DataFrame for the "Last touchpoints" pivot
    query_last_touchpoints = """
    WITH tmp_number_steps AS (
        SELECT *,
            step_no = ROW_NUMBER() over (PARTITION BY interaction_id ORDER BY category)
            FROM jps.talkdesk_ivr_studio
            WHERE type_of_call = 'Main Menu'
    )
    SELECT CONVERT(date, SWITCHOFFSET(started_at_utc, '-05:00')) AS date,
        interaction_id,
        category,
        subcategory
        FROM tmp_number_steps a
        WHERE step_no = (SELECT MAX(step_no)
                            FROM tmp_number_steps b
                            WHERE b.interaction_id = a.interaction_id)
        AND MONTH(CONVERT(date, SWITCHOFFSET(started_at_utc, '-05:00'))) = MONTH(GETDATE())
        AND YEAR(CONVERT(date, SWITCHOFFSET(started_at_utc, '-05:00'))) = YEAR(GETDATE());
    """

    df_last_touchpoints = pd.read_sql(query_last_touchpoints, conn)
    pivot_last = pd.pivot_table(df_last_touchpoints,
                                index=["category", "subcategory"],
                                columns="date",
                                aggfunc=len,
                                margins=True,
                                margins_name="Total")

    # Find the maximum month from the "date" column
    max_month = df['date'].max().strftime('%B')

    # Save both pivot tables to Excel
    excel_writer = pd.ExcelWriter("src\\jps\\Touchpoints report.xlsx", engine="xlsxwriter")

    pivot_all.to_excel(excel_writer, sheet_name="All touchpoints", index=True)
    pivot_last.to_excel(excel_writer, sheet_name="Call termination", index=True)

    excel_writer.save()

    # Additional code for Datascience Hub and file naming
    ctx = shwp.get_datascience_hub_ctx()
    touchpoints_folder_id = utils.get_config("dshub_sharepoint_config")["folders"]["jps_touchpoints"]["id"]
    file_path = "src\\jps\\Touchpoints report.xlsx"
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
