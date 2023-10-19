""" 
Downloads an Excel file containing actual hours and calls from the SharePoint and uploads to the database.
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

    # Fill empty values with NULLs
    df = dfutils.fill_dataframe_nulls(df, '-')

    print('Truncating database and reinserting.')
    # Truncate and insert into the database
    dbutils.perform_safe_truncate_insert(df, conn, schema, table_name)

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """

    match optional[0]:
        case 1:
            sheet_name = 'MBJ'
            table_name = 'mbj_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'active_engage'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['active_engage_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['active_engage_daily_billable_hours']['name']
        case 2:
            sheet_name = None
            table_name = 'glb_daily_billable_minutes'
            expected_columns = ['date', 'billable_production_minutes', 'billable_training_minutes']
            schema = 'btc'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['btc_daily_billable_minutes']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['btc_daily_billable_minutes']['name']
        case 3:
            sheet_name = 'MBJ'
            table_name = 'mbj_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'harry_and_david'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['harry_and_david_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['harry_and_david_daily_billable_hours']['name']
        case 4:
            sheet_name = 'GEO'
            table_name = 'geo_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'harry_and_david'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['harry_and_david_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['harry_and_david_daily_billable_hours']['name']
        case 5:
            sheet_name = 'MBJ'
            table_name = 'mbj_daily_handled_calls'
            expected_columns = ['date', 'handled_sales_calls', 'handled_service_calls', 'handled_guest_assurance_calls',
            'handled_diamond_calls', 'billable_training_hours']
            schema = 'hilton'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['hilton_daily_handled_calls']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['hilton_daily_handled_calls']['name']
        case 6:
            sheet_name = 'KGN'
            table_name = 'kgn_daily_handled_calls'
            expected_columns = ['date', 'handled_sales_calls', 'handled_service_calls', 'handled_guest_assurance_calls',
            'handled_diamond_calls', 'billable_training_hours']
            schema = 'hilton'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['hilton_daily_handled_calls']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['hilton_daily_handled_calls']['name']
        case 7:
            sheet_name = 'SLU'
            table_name = 'slu_daily_handled_calls'
            expected_columns = expected_columns = ['date', 'handled_sales_calls', 'handled_service_calls', 'handled_guest_assurance_calls',
            'handled_diamond_calls', 'billable_training_hours']
            schema = 'hilton'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['hilton_daily_handled_calls']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['hilton_daily_handled_calls']['name']
        case 8:
            sheet_name = 'WAH'
            table_name = 'glb_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'homesite'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['home_site_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['home_site_daily_billable_hours']['name']
        case 9:
            sheet_name = 'WAH'
            table_name = 'glb_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_bilingual_hours', 'billable_supervisor_hours', 'billable_sdr_usa_hours', 'billable_training_hours','ancillary_revenue_usd']
            schema = 'run_buggy'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['run_buggy_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['run_buggy_daily_billable_hours']['name']
        case 10:
            sheet_name = 'WAH'
            table_name = 'wah_blended_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours','billable_overtime_hours']
            schema = 'the_general'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['the_general_blended_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['the_general_blended_daily_billable_hours']['name']
        case 11:
            sheet_name = 'WAH'
            table_name = 'wah_customer_service_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'the_general'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['the_general_customer_service_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['the_general_customer_service_daily_billable_hours']['name']
        case 12:
            sheet_name = 'BAH'
            table_name = 'bah_customer_service_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'the_general'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['the_general_customer_service_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['the_general_customer_service_daily_billable_hours']['name']
        case 13:
            sheet_name = 'SLU'
            table_name = 'slu_daily_billable_hours'
            expected_columns = ['date', 'phone_billable_hours', 'chat_billable_hours', 'vitacost_billable_hours',
            'vitacost_phone_billable_hours', 'core_billable_hours', 'core_voice_billable_hours', 'billable_training_hours']
            schema = 'kroger'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['kroger_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['kroger_daily_billable_hours']['name']
        case 14:
            sheet_name = 'KGN'
            table_name = 'kgn_daily_billable_hours'
            expected_columns = ['date', 'phone_billable_hours', 'chat_billable_hours', 'vitacost_billable_hours',
            'vitacost_phone_billable_hours', 'core_billable_hours', 'core_voice_billable_hours', 'billable_training_hours']
            schema = 'kroger'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['kroger_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['kroger_daily_billable_hours']['name']
        case 15:
            sheet_name = 'SLU'
            table_name = 'slu_daily_billable_hours'
            expected_columns = ['date', 'billable_shutterfly_hours', 'billable_lifetouch_hours',
            'billable_training_hours']
            schema = 'lifetouch_shutterfly'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['shutterfly_lifetouch_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['shutterfly_lifetouch_daily_billable_hours']['name']
        case 16:
            sheet_name = 'KGN'
            table_name = 'kgn_daily_billable_hours'
            expected_columns = ['date', 'billable_shutterfly_hours', 'billable_lifetouch_hours',
            'billable_shutterfly_training_hours', 'billable_lifetouch_training_hours']
            schema = 'lifetouch_shutterfly'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['shutterfly_lifetouch_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['shutterfly_lifetouch_daily_billable_hours']['name']
        case 17:
            sheet_name = None
            table_name = 'glb_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'louis_vuitton'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['louis_vuitton_daily_worked_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['louis_vuitton_daily_worked_hours']['name']
        case 18:
            sheet_name = None
            table_name = 'glb_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours','billable_overtime_hours']
            schema = 'ancestry'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['ancestry_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['ancestry_daily_billable_hours']['name']
        case 19:
            sheet_name = 'MBJ'
            table_name = 'mbj_daily_billable_hours'
            expected_columns = ['date', 'billable_production_minutes', 'billable_training_hours']
            schema = 'one_eight_hundred_flowers'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['one_eight_hundred_flowers_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['one_eight_hundred_flowers_daily_billable_hours']['name']
        case 20:
            sheet_name = None
            table_name = 'glb_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'bmot'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['bmot_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['bmot_daily_billable_hours']['name']
        case 21:
            sheet_name = None
            table_name = 'glb_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'breville'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['breville_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['breville_daily_billable_hours']['name']   
        case 22:
            sheet_name = None
            table_name = 'glb_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'bradford'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['bradford_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['bradford_daily_billable_hours']['name']    
        case 23:
            sheet_name = None
            table_name = 'glb_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'car_rental_eight'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['car_rental_eight_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['car_rental_eight_daily_billable_hours']['name']
        case 24:
            sheet_name = None
            table_name = 'glb_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'carey'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['carey_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['carey_daily_billable_hours']['name']
        case 25:
            sheet_name = 'JPS KGN'
            table_name = 'kgn_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'jps'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['jps_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['jps_daily_billable_hours']['name'] 
        case 26:
            sheet_name = 'JPS MBJ'
            table_name = 'mbj_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'jps'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['jps_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['jps_daily_billable_hours']['name']
        case 27:
            sheet_name = 'Speedy MBJ'
            table_name = 'mbj_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'speedy'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['speedy_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['speedy_daily_billable_hours']['name']   
        case 28:
            sheet_name = 'Speedy SLU'
            table_name = 'slu_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'speedy'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['speedy_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['speedy_daily_billable_hours']['name']  
        case 29:
            sheet_name = None
            table_name = 'glb_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'ontellus'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['ontellus_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['ontellus_daily_billable_hours']['name']
        case 30:
            sheet_name = None
            table_name = 'glb_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'psn'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['psn_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['psn_daily_billable_hours']['name']  
        case 31:
            sheet_name = 'GEO'
            table_name = 'geo_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'active_engage'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['active_engage_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['active_engage_daily_billable_hours']['name']
        case 32:
            sheet_name = 'AH GEO'
            table_name = 'geo_daily_billable_training_hours'
            expected_columns = ['date', 'billable_training_hours']
            schema = 'anyone_home'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['anyone_home_daily_billable_training_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['anyone_home_daily_billable_training_hours']['name']
        case 33:
            sheet_name = 'AH SAP'
            table_name = 'sap_daily_billable_training_hours'
            expected_columns = ['date', 'billable_training_hours', 'billable_wfm_hours']
            schema = 'anyone_home'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['anyone_home_daily_billable_training_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['anyone_home_daily_billable_training_hours']['name']
        case 34:
            sheet_name = 'KGN'
            table_name = 'kgn_daily_billable_training_hours'
            expected_columns = ['date', 'billable_training_hours']
            schema = 'altice'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['altice_daily_billable_training_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['altice_daily_billable_training_hours']['name']
        case 35:
            sheet_name = 'MBJ'
            table_name = 'mbj_daily_billable_training_hours'
            expected_columns = ['date', 'billable_training_hours']
            schema = 'altice'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['altice_daily_billable_training_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['altice_daily_billable_training_hours']['name']
        case 36:
            sheet_name = 'SLU'
            table_name = 'slu_daily_billable_training_hours'
            expected_columns = ['date', 'billable_training_hours']
            schema = 'altice'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['altice_daily_billable_training_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['altice_daily_billable_training_hours']['name']
        case 37:
            sheet_name = 'GEO'
            table_name = 'glb_daily_billable_training_hours'
            expected_columns = ['date', 'billable_training_hours']
            schema = 'liveperson'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['liveperson_daily_billable_training_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['liveperson_daily_billable_training_hours']['name']
        case 38:
            sheet_name = 'GEO'
            table_name = 'geo_daily_billable_training_hours'
            expected_columns = ['date', 'billable_training_hours', 'daily_ancillary_revenue_usd']
            schema = 'office_depot'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['office_depot_daily_billable_training_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['office_depot_daily_billable_training_hours']['name']
        case 39:
            sheet_name = 'WAH'
            table_name = 'wah_daily_billable_training_hours'
            expected_columns = ['date', 'billable_training_hours']
            schema = 'office_depot'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['office_depot_daily_billable_training_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['office_depot_daily_billable_training_hours']['name']
        case 40:
            sheet_name = 'KGN'
            table_name = 'kgn_daily_billable_hours'
            expected_columns = ['date', 'billable_day_production_hours', 'billable_night_production_hours','billable_training_hours']
            schema = 'iaa'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['iaa_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['iaa_daily_billable_hours']['name'] 
        case 41:
            sheet_name = 'SAP'
            table_name = 'sap_daily_billable_training_hours'
            expected_columns = ['date','billable_training_hours']
            schema = 'walmart'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['walmart_daily_billable_training_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['walmart_daily_billable_training_hours']['name']
        case 42:
            sheet_name = 'MBJ'
            table_name = 'mbj_field_services_daily_billable_hours'
            expected_columns = ['date','billable_field_services_hours', 'billable_training_hours']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_field_services_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['tds_field_services_daily_billable_hours']['name']
        case 43:
            sheet_name = 'MBJ'
            table_name = 'mbj_financial_services_daily_billable_hours'
            expected_columns = ['date','billable_financial_services_tier_one_hours','billable_financial_services_tier_two_hours', 'billable_training_hours']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_financial_services_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['tds_financial_services_daily_billable_hours']['name']
        case 44:
            sheet_name = 'SLU'
            table_name = 'slu_financial_services_daily_billable_hours'
            expected_columns = ['date','billable_financial_services_tier_one_hours','billable_financial_services_tier_two_hours', 'billable_training_hours']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_financial_services_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['tds_financial_services_daily_billable_hours']['name']
        case 45:
            sheet_name = 'MBJ'
            table_name = 'mbj_repair_daily_billable_hours'
            expected_columns = ['date','billable_consumer_hours','billable_commercial_hours','billable_daart_hours','billable_augmented_coach_hours','billable_training_hours']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_repair_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['tds_repair_daily_billable_hours']['name']            
        case 46:
            sheet_name = 'SLU'
            table_name = 'slu_repair_daily_billable_hours'
            expected_columns = ['date', 'billable_consumer_hours','billable_commercial_hours','billable_daart_hours','billable_augmented_coach_hours','billable_training_hours']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_repair_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['tds_repair_daily_billable_hours']['name']
        case 47:
            sheet_name = 'MBJ'
            table_name = 'mbj_sales_daily_billable_hours'
            expected_columns = ['date','billable_sales_hours','billable_customer_service_hours', 'billable_training_hours']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_sales_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['tds_sales_daily_billable_hours']['name']
        case 48:
            sheet_name = 'SLU'
            table_name = 'slu_sales_daily_billable_hours'
            expected_columns = ['date','billable_sales_hours','billable_customer_service_hours', 'billable_training_hours']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_sales_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['tds_sales_daily_billable_hours']['name']            
        case 49:
            sheet_name = 'GEO'
            table_name = 'geo_daily_billable_hours'
            expected_columns = ['date','billable_production_hours', 'billable_training_hours']
            schema = 'maxsold'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['maxsold_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['maxsold_daily_billable_hours']['name']
        case 50:
            sheet_name = 'MBJ'
            table_name = 'mbj_daily_billable_hours'
            expected_columns = ['date','billable_production_hours', 'billable_training_hours']
            schema = 'ministry_health'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['ministry_health_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['ministry_health_daily_billable_hours']['name']
        case 51:
            sheet_name = 'MBJ'
            table_name = 'mbj_daily_billable_training_hours'
            expected_columns = ['date', 'billable_training_hours']
            schema = 'liveperson'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['liveperson_daily_billable_training_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['liveperson_daily_billable_training_hours']['name']
        case 52:
            sheet_name = 'GEO'
            table_name = 'geo_daily_handled_calls'
            expected_columns = expected_columns = ['date', 'handled_sales_calls', 'handled_service_calls', 'handled_guest_assurance_calls',
            'handled_diamond_calls','billable_email_hours','billable_training_hours']
            schema = 'hilton'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['hilton_daily_handled_calls']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['hilton_daily_handled_calls']['name']
        case 53:
            sheet_name = 'KGN'
            table_name = 'kgn_customer_service_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours','billable_overtime_hours']
            schema = 'the_general'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['the_general_customer_service_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['the_general_customer_service_daily_billable_hours']['name']
        case 54:
            sheet_name = 'KGN'
            table_name = 'kgn_daily_billable_hours'
            expected_columns = ['date', 'billable_production_minutes', 'billable_training_hours']
            schema = 'one_eight_hundred_flowers'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['one_eight_hundred_flowers_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['one_eight_hundred_flowers_daily_billable_hours']['name']
        case 55:
            sheet_name = 'AH BZE'
            table_name = 'bze_daily_billable_training_hours'
            expected_columns = ['date', 'billable_training_hours']
            schema = 'anyone_home'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['anyone_home_daily_billable_training_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['anyone_home_daily_billable_training_hours']['name'] 
        case 56:
            sheet_name = 'TCC JLP KGN'
            table_name = 'kgn_tcc_jlp_daily_billable_hours'
            expected_columns = ['date','billable_production_hours', 'billable_training_hours']
            schema = 'tcc_jlp'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tcc_jlp_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['tcc_jlp_daily_billable_hours']['name']  
        case 57: 
            sheet_name = 'KGN'
            table_name = 'kgn_ccc_daily_billable_hours'
            expected_columns = ['date','billable_production_hours', 'billable_production_claim', 'billable_training_hours']
            schema = 'ccc'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['ccc_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['ccc_daily_billable_hours']['name'] 
        case 58: 
            sheet_name = 'KGN'
            table_name = 'kgn_mia_daily_billable_hours'
            expected_columns = ['date','billable_concierge_hours','billable_concierge_training_hours','billable_sales_hours',
                                'billable_sales_training_hours',"billable_post_op_hours","billable_post_op_premiun_hours",
                                "billable_post_op_training_hours"]
            schema = 'mia'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['mia_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['mia_daily_billable_hours']['name']
        case 59:
            sheet_name = 'GUY'
            table_name = 'geo_daily_billable_hours'
            expected_columns = ['date', 'phone_billable_hours', 'chat_billable_hours', 'vitacost_billable_hours',
            'vitacost_phone_billable_hours', 'core_billable_hours', 'core_voice_billable_hours', 'billable_training_hours']
            schema = 'kroger'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['kroger_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['kroger_daily_billable_hours']['name']
        case 60:
            sheet_name = 'MBJ'
            table_name = 'mbj_com_daily_billable_hours'
            expected_columns = ['date','billable_production_hours', 'billable_training_hours']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_com_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['tds_com_daily_billable_hours']['name']
        case 61:
            sheet_name = 'BZE'
            table_name = 'bze_daily_billable_hours'
            expected_columns = ['date','billable_production_hours', 'billable_training_hours']
            schema = 'epremium'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['epremium_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['epremium_daily_billable_hours']['name']
        case 62:
            sheet_name = 'SAP'
            table_name = 'sap_daily_billable_hours'
            expected_columns = ["date","billable_production_csr1_hours","billable_production_csr2_hours","billable_training_csr1_hours","billable_training_csr2_hours"]
            schema = 'henry_schein'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['henry_schein_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['henry_schein_daily_billable_hours']['name']
        case 63:
            sheet_name = 'MBJ'
            table_name = 'mbj_daily_billable_hours'
            expected_columns = ["date","billable_production_hours","billable_training_hours"]
            schema = 'auto_europe'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['auto_europe_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['auto_europe_daily_billable_hours']['name']
        case 64:
            sheet_name = 'SLU'
            table_name = 'slu_daily_billable_hours'
            expected_columns = ["date","billable_production_res_tier_one_calls","billable_production_res_tier_two_calls","billable_production_cus_calls","billable_training_hours"]
            schema = 'avis'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['avis_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['avis_daily_billable_hours']['name']
        case 65:
            sheet_name = 'KGN'
            table_name = 'kgn_daily_billable_hours'
            expected_columns = ["date","billable_production_res_tier_one_calls","billable_production_res_tier_two_calls","billable_production_cus_calls","billable_training_hours"]
            schema = 'avis'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['avis_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['avis_daily_billable_hours']['name']
        case 66:
            sheet_name = 'KGN'
            table_name = 'kgn_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'active_engage'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['active_engage_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['active_engage_daily_billable_hours']['name']
        case 67:
            sheet_name = 'KGN'
            table_name = 'kgn_daily_billable_hours'
            expected_columns = ['date', 'billable_production_hours', 'billable_training_hours']
            schema = 'homesite'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['home_site_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['home_site_daily_billable_hours']['name']
        case 68: 
            sheet_name = 'BZE'
            table_name = 'bze_mia_daily_billable_hours'
            expected_columns = ['date','billable_production_hours','billable_training_hours']
            schema = 'mia'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['mia_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['mia_daily_billable_hours']['name']
        case 69:
            sheet_name = 'MBJ'
            table_name = 'mbj_cno_daily_billable_hours'
            expected_columns = ['date','billable_production_hours', 'billable_training_hours']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_cno_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['tds_cno_daily_billable_hours']['name']
        case 70:
            sheet_name = 'SLU'
            table_name = 'slu_daily_billable_hours'
            expected_columns = ['date', 'billable_sdr_stl_hours','billable_sdr_training_hours']
            schema = 'run_buggy'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['run_buggy_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['run_buggy_daily_billable_hours']['name']
        case 71:
            sheet_name = 'SAP'
            table_name = 'sap_daily_billable_hours'
            expected_columns = ["date","billable_production_hours","billable_training_hours"]
            schema = 'goals'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['goals_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['goals_daily_billable_hours']['name']
        case 72:
            sheet_name = 'GEO'
            table_name = 'geo_daily_billable_hours'
            expected_columns = ['date','billable_production_hours', 'billable_training_hours']
            schema = 'epremium'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['epremium_daily_billable_hours']['id']
            file_name = utils.get_config('dshub_sharepoint_config')['files']['epremium_daily_billable_hours']['name']

    print(f'Uploading {file_name}')
    sheet_downloader_and_uploader(table_name, expected_columns, schema, file_id, sheet_name)
