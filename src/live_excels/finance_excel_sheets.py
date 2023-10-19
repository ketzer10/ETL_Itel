""" 
Downloads an Excel file containing ancillary and training revenues per line of business.
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

    print('Getting SharePoint context.')
    ctx = shwp.get_datascience_hub_ctx()
    print('Opening database connection.') # Get Data Science Hub SharePoint context
    conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
    print('Getting file from SharePoint site.')    
    file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
    print('Loading Excel file into pandas DataFrame.')
    
    # If no sheet name was passed, just read the first tab of the sheet. Otherwise read the passed name
    if sheet_name is None:
        df = pd.read_excel(file_obj['contents']) # Read into a DataFrame
    else:
        df = pd.read_excel(file_obj['contents'], sheet_name=sheet_name) # Read into a DataFrame

    # Verify that expected columns match the actual dataframe columns
    assert expected_columns == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'

    # Fill empty values with None
    df = dfutils.fill_dataframe_nulls(df, '')
    
    print('Truncating database and reinserting.')
    # Truncate and insert into the database
    dbutils.perform_safe_truncate_insert(df, conn, schema, table_name)


def main(optional: list = None):
    """ Runs the sheet_downloader_and_uploader.
    """

    match optional[0]:
        case 1: # Global month end closing revenue
            sheet_name = 'unpivoted_actual_rev'
            table_name = 'glb_closing_revenue'
            expected_columns = ['business_unit', 'month_starting', 'revenue_usd']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['month_end_closing_revenue']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['month_end_closing_revenue']['name']

            print(f'Uploading {file_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)
        case 2: # Global budgeted revenue
            sheet_name = 'unpivoted_budgeted_revenue'
            table_name = 'glb_budgeted_revenue_by_business_unit'
            expected_columns = ['month_starting', 'business_unit', 'monthly_budgeted_usd', 'daily_budgeted_usd']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['business_unit_budgets']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['business_unit_budgets']['name']

            print(f'Uploading {file_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)
        case 3: # Ancillary revenue
            sheet_name = 'ancillary_revenue'
            table_name = 'glb_ancillary_revenue_streams'
            expected_columns = ['month_starting', 'business_unit', 'daily_ancillary_revenue_usd', 'daily_training_revenue_usd']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['business_unit_ancillary_training_revenue']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['business_unit_ancillary_training_revenue']['name']

            print(f'Uploading {file_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)
        case 4: # Billable rates
            sheet_name = None
            table_name = 'glb_business_unit_billable_rates'
            expected_columns = ['business_unit', 'rate_code_lob', 'billing_type', 'rate', 'start_date', 'end_date',
            'operations_training', 'comments']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['business_unit_billable_rates']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['business_unit_billable_rates']['name']
            print(f'Uploading {file_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)
        case 5: # Outlook Lock forecast by Business Unit
            sheet_name = 'unpivoted_locked_forecast'
            table_name = 'glb_outlook_revenue'
            expected_columns = ['month_starting', 'business_unit', 'monthly_budgeted_usd', 'daily_budgeted_usd']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['outlook_locked_forecast']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['outlook_locked_forecast']['name']        

            print(f'Uploading {file_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)
        case 6: # Closing monthly payroll
            sheet_name = 'unpivoted_closing_payroll'
            table_name = 'glb_closing_payroll'
            expected_columns = ['business_unit', 'month_starting', 'monthly_payroll_usd', 'daily_payroll_usd']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['monthly_closing_payroll']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['monthly_closing_payroll']['name']        

            print(f'Uploading {file_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)
        case 7: # Budgeted payroll
            sheet_name = 'unpivoted_budgeted_payroll'
            table_name = 'glb_budgeted_payroll'
            expected_columns = ['month_starting', 'business_unit', 'monthly_budgeted_usd', 'daily_budgeted_usd']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['monthly_budgeted_payroll']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['monthly_budgeted_payroll']['name']
            print(f'Uploading {file_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)
        case 8: # Payroll adjustment factors
            sheet_name = 'Adjustments'
            table_name = 'payroll_adjustment_factors'
            expected_columns = ['business_unit', 'tax_factor', 'adjustment_factor', 'start_date', 'end_date']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['payroll_adjustment_factors']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['payroll_adjustment_factors']['name']
            print(f'Uploading {file_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)
        case 9: # Payroll additions
            sheet_name = 'Additions'
            table_name = 'payroll_addition_factors'
            expected_columns = ['business_unit', 'month_starting', 'monthly_addition_usd', 'daily_addition_usd']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['payroll_adjustment_factors']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['payroll_adjustment_factors']['name']      

            print(f'Uploading {file_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)
        case 10: # Budgeted Billable Hours
            sheet_name = 'unpivoted_budget_billable_hour'
            table_name = 'glb_budgeted_billable_hours_by_business_unit'
            expected_columns = ['month_starting', 'business_unit', 'monthly_budgeted_billable_hours', 'daily_budgeted_billable_hours']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['budgeted_payroll_and_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['budgeted_payroll_and_billable_hours']['name']      

            print(f'Uploading {file_name}, {sheet_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)

        case 11: # Budgeted Payroll Hours
            sheet_name = 'unpivoted_budget_payroll_hours'
            table_name = 'glb_budgeted_payroll_hours_by_business_unit'
            expected_columns = ['month_starting', 'business_unit', 'monthly_budgeted_payroll_hours', 'daily_budgeted_payroll_hours']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['budgeted_payroll_and_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['budgeted_payroll_and_billable_hours']['name']      

            print(f'Uploading {file_name}, {sheet_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)

        case 12: # Budgeted Agent Hours
            sheet_name = 'unpivot_budget_agent_hours'
            table_name = 'glb_budgeted_agent_hours_by_business_unit'
            expected_columns = ['month_starting', 'business_unit', 'monthly_budgeted_agent_hours', 'daily_budgeted_agent_hours']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['budgeted_payroll_and_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['budgeted_payroll_and_billable_hours']['name']      

            print(f'Uploading {file_name}, {sheet_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)

        case 13: # Budgeted Unbillable Training Hours
            sheet_name = 'unpivot_budget_training_nb'
            table_name = 'glb_budgeted_training_unbillable_hours_by_business_unit'
            expected_columns = ['month_starting', 'business_unit', 'monthly_budgeted_training_unbillable_hours', 'daily_budgeted_training_unbillable_hours']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['budgeted_payroll_and_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['budgeted_payroll_and_billable_hours']['name']      

            print(f'Uploading {file_name}, {sheet_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)

        case 14: # Budgeted Billable Training Hours
            sheet_name = 'unpivot_budget_training_b'
            table_name = 'glb_budgeted_training_billable_hours_by_business_unit'
            expected_columns = ['month_starting', 'business_unit', 'monthly_budgeted_training_billable_hours', 'daily_budgeted_training_billable_hours']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['budgeted_payroll_and_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['budgeted_payroll_and_billable_hours']['name']      

            print(f'Uploading {file_name}, {sheet_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)

        case 15: # Budgeted Billable Production Hours
            sheet_name = 'unpivot_budget_billable_ph'
            table_name = 'glb_budgeted_production_billable_hours_by_business_unit'
            expected_columns = ['month_starting', 'business_unit', 'monthly_budgeted_billable_prod_hours', 'daily_budgeted_billable_prod_hours']
            schema = 'finance'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['budgeted_payroll_and_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['budgeted_payroll_and_billable_hours']['name']      

            print(f'Uploading {file_name}, {sheet_name}')
            sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)            