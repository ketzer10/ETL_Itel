""" 
Downloads an Excel file containing payroll information for Honduras.
"""

import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils

def sheet_downloader_and_uploader(table_name: str, expected_columns: list, schema: str, file_id: str, sheet_name: str = None):
    """Truncates and uploads a forecast live Excel files to the database. 
    Args:
        table_name (str): The name of the table to upload to. 
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        file_id (str): ID for the file in sharepoint
        sheet_name (str): Optional argument that specifies the sheet name. Only one sheet name can be passed. If no argument 
        is passed, the first sheet of the Excel workbook is read.
    """

    print("Getting SharePoint context.")
    ctx = shwp.get_datascience_hub_ctx()
    print("Opening database connection.") # Get Data Science Hub SharePoint context
    conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
    print("Getting file from SharePoint site.")    
    file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
    print("Loading Excel file into pandas DataFrame.")
    
    # If no sheet name was passed, just read the first tab of the sheet. Otherwise read the passed name
    if sheet_name is None:
        df = pd.read_excel(file_obj["contents"]) # Read into a DataFrame
    else:
        df = pd.read_excel(file_obj["contents"], sheet_name=sheet_name) # Read into a DataFrame

    print(df)
    df = df[expected_columns]
    print(df)

    # Verify that expected columns match the actual dataframe columns
    assert expected_columns == df.columns.tolist(), "Expected columns do not match actual dataframe columns"

    # Fill empty values with NULLs
    df = dfutils.fill_dataframe_nulls(df, "-")

    print("Truncating database and reinserting.")
    # Truncate and insert into the database
    dbutils.perform_safe_truncate_insert(df, conn, schema, table_name)

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """

    match optional[0]:
        case 1:
            sheet_name = None
            table_name = "sap_support_staff_overtime"
            expected_columns = ["legacy_id", "employee_name", "date", "ot_hours", "ot_shift"]
            schema = "hr"
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["sap_support_staff_overtime"]["id"]
            file_name = utils.get_config("dshub_sharepoint_config")["files"]["sap_support_staff_overtime"]["name"]
        case 2:
            sheet_name = None
            table_name = "sap_payroll_allowances"
            expected_columns = ["payroll_start_date", "legacy_id", "employee_name", "allowance_usd"]
            schema = "hr"
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["sap_support_staff_payroll_allowances"]["id"]
            file_name = utils.get_config("dshub_sharepoint_config")["files"]["sap_support_staff_payroll_allowances"]["name"]
        case 3:
            sheet_name = None
            table_name = "sap_payroll_bonuses"
            expected_columns = ["payroll_start_date", "legacy_id", "employee_name", "bonus_type", "bonus_usd"]
            schema = "hr"
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["sap_payroll_bonuses"]["id"]
            file_name = utils.get_config("dshub_sharepoint_config")["files"]["sap_payroll_bonuses"]["name"]
        case 4:
            sheet_name = None
            table_name = "sap_support_staff_worked_time"
            expected_columns = ["date", "legacy_id", "full_name", "hours"]
            schema = "hr"
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["sap_support_staff_worked_time"]["id"]
            file_name = utils.get_config("dshub_sharepoint_config")["files"]["sap_support_staff_worked_time"]["name"]
        case 5: 
            sheet_name = "Deductions"
            table_name = "sap_payroll_deductions"
            expected_columns = ["legacy_id", "employee_name", "payroll_start_date", "deduction_type", "deduction_usd"]
            schema = "hr"
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["sap_payroll_deductions"]["id"]
            file_name = utils.get_config("dshub_sharepoint_config")["files"]["sap_payroll_deductions"]["name"]        
        case 6: 
            sheet_name = "Income"
            table_name = "sap_payroll_other_income_sources"
            expected_columns = ["legacy_id", "employee_name", "payroll_start_date", "pay_code", "units", "code_value"]
            schema = "hr"
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["sap_other_income_sources"]["id"]
            file_name = utils.get_config("dshub_sharepoint_config")["files"]["sap_other_income_sources"]["name"]                  

    print(f"Uploading {file_name}")
    sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)