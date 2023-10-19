""" 
Downloads an Excel file containing forecasts from the SharePoint and uploads to the database.  
"""

import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils

def sheet_downloader_and_uploader(sheet_name: str, table_name: str, expected_columns: list, schema: str, file_id: str):
    """Truncates and uploads a forecast live Excel files to the database. 
    Args:
        sheet_name (str): The name of the sheet on the file to be uploaded.  
        table_name (str): The name of the table to upload to. 
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        file_id (str): ID for the file in sharepoint
    """
    print('Getting SharePoint context.')
    ctx = shwp.get_datascience_hub_ctx()
    print('Opening database connection.') # Get Data Science Hub SharePoint context
    conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
    print('Getting file from SharePoint site.')    
    file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
    print('Loading Excel file into pandas DataFrame.')
    df = pd.read_excel(file_obj['contents'], sheet_name=sheet_name) # Read into a DataFrame

    # Verify that expected columns match the actual dataframe columns
    assert expected_columns == df.columns.tolist(), 'Expected columns do not match actual dataframe columns'

    # Fill empty values with NULLS 
    df = dfutils.fill_dataframe_nulls(df, '')

    print('Truncating database and reinserting.')
    # Truncate and insert into the database
    dbutils.perform_safe_truncate_insert(df, conn, schema, table_name)

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """

    match optional[0]:
        # Walmart          
        case 1:
            sheet_name = 'SAP Forecast'
            table_name = 'sap_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_inbound_billable_calls', 'wfm_outbound_billable_calls', 'wfm_billable_classroom_training_hours', 'wfm_ancillary_revenue_usd',
                                'client_inbound_billable_calls', 'client_outbound_billable_calls','client_billable_classroom_training_hours', 'client_ancillary_revenue_usd']
            schema = 'walmart'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['walmart_forecasted_calls_hours']['id']
        case 2:
            sheet_name = 'KGN Forecast'
            table_name = 'kgn_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_inbound_billable_calls', 'wfm_outbound_billable_calls', 'wfm_billable_classroom_training_hours', 'wfm_ancillary_revenue_usd',
                                'client_inbound_billable_calls', 'client_outbound_billable_calls','client_billable_classroom_training_hours', 'client_ancillary_revenue_usd']
            schema = 'walmart'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['walmart_forecasted_calls_hours']['id'] 
        #Active Engage
        case 3:
            sheet_name = 'MBJ'
            table_name = 'mbj_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 'client_billable_training_hours', 
                                'client_ancillary_revenue_usd']
            schema = 'active_engage'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['active_engage_forecasted_calls_hours']['id']       
        # Altice
        case 4:
            sheet_name = 'Altice KGN'
            table_name = 'kgn_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'altice'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['altice_forecasted_calls_hours']['id']
        case 5:
            sheet_name = 'Altice MBJ'
            table_name = 'mbj_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'altice'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['altice_forecasted_calls_hours']['id']
        case 6:
            sheet_name = 'Altice SLU'
            table_name = 'slu_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'altice'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['altice_forecasted_calls_hours']['id']         
        # Ancestry
        case 7:
            sheet_name = 'Ancestry Forecast'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd','wfm_billable_overtime_hours',
                                'client_billable_overtime_hours']
            schema = 'ancestry'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['ancestry_forecasted_calls_hours']['id']
        # BMOT
        case 8:
            sheet_name = 'BMOT Forecast'
            table_name = 'glb_calls_and_hours_forecast' 
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'bmot'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['bmot_forecasted_calls_hours']['id']        
        # Bradford
        case 9:
            sheet_name = 'Bradford Forecast'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'bradford'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['bradford_forecasted_calls_hours']['id']
        # Breville
        case 10:
            sheet_name = 'Breville Forecast'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'breville'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['breville_forecasted_calls_hours']['id']
        # Anyone Home 
        case 11:
            sheet_name = 'Anyone Home Guyana'
            table_name = 'geo_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 'wfm_ancillary_revenue_usd',
                                'client_billable_production_hours', 'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'anyone_home'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['anyone_home_forecasted_calls_hours']['id']
        case 12:
            sheet_name = 'Anyone Home Honduras'
            table_name = 'sap_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 'wfm_billable_wfm_hours',
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 'client_billable_training_hours', 
                                'client_billable_wfm_hours', 'client_ancillary_revenue_usd']
            schema = 'anyone_home'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['anyone_home_forecasted_calls_hours']['id']   
        # 1800 flowers MBJ
        case 13:
            sheet_name = 'MBJ'
            table_name = 'mbj_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_mins', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_mins', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'one_eight_hundred_flowers'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['one_eight_hundred_flowers_forecasted_calls_hours']['id']
        # BTC
        case 14:
            sheet_name = 'BTC Forecast'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_mins', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_mins', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'btc'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['btc_forecasted_calls_hours']['id']
        # Car Rental 8
        case 15:
            sheet_name = 'Car Rental 8 Forecast'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'car_rental_eight'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['car_rental_eight_forecasted_calls_hours']['id']
        # Carey
        case 16:
            sheet_name = 'Carey Forecast'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'carey'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['carey_forecasted_calls_hours']['id']  
        # Harry and David
        case 17:
            sheet_name = 'Harry and David MBJ'
            table_name = 'mbj_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 'wfm_ancillary_revenue_usd',
            'client_billable_production_hours', 'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'harry_and_david'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['harry_and_david_forecasted_calls_hours']['id']
        case 18:
            sheet_name = 'Harry and David GEO'
            table_name = 'geo_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 'wfm_ancillary_revenue_usd',
            'client_billable_production_hours', 'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'harry_and_david'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['harry_and_david_forecasted_calls_hours']['id'] 
        # Hilton
        case 19:
            sheet_name = 'KGN'
            table_name = 'kgn_calls_and_hours_forecast'
            expected_columns = ['date','wfm_billable_reservation_calls','wfm_billable_guest_assurance_calls',
                                'wfm_billable_diamond_calls','wfm_billable_customer_care_calls',
                                'wfm_billable_training_hours','wfm_ancillary_revenue_usd',
                                'client_billable_reservation_calls','client_billable_guest_assurance_calls',
                                'client_billable_diamond_calls','client_billable_customer_care_calls',
                                'client_billable_training_hours','client_ancillary_revenue_usd']
            schema = 'hilton'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['hilton_forecasted_calls_hours']['id']
        case 20:
            sheet_name = 'MBJ'
            table_name = 'mbj_calls_and_hours_forecast'
            expected_columns = ['date','wfm_billable_reservation_calls','wfm_billable_guest_assurance_calls',
                                'wfm_billable_diamond_calls','wfm_billable_customer_care_calls',
                                'wfm_billable_training_hours','wfm_ancillary_revenue_usd',
                                'client_billable_reservation_calls','client_billable_guest_assurance_calls',
                                'client_billable_diamond_calls','client_billable_customer_care_calls',
                                'client_billable_training_hours','client_ancillary_revenue_usd']
            schema = 'hilton'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['hilton_forecasted_calls_hours']['id']  
        case 21:
            sheet_name = 'SLU'
            table_name = 'slu_calls_and_hours_forecast'
            expected_columns = ['date','wfm_billable_reservation_calls','wfm_billable_guest_assurance_calls',
                                'wfm_billable_diamond_calls','wfm_billable_customer_care_calls',
                                'wfm_billable_training_hours','wfm_ancillary_revenue_usd',
                                'client_billable_reservation_calls','client_billable_guest_assurance_calls',
                                'client_billable_diamond_calls','client_billable_customer_care_calls',
                                'client_billable_training_hours','client_ancillary_revenue_usd']
            schema = 'hilton'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['hilton_forecasted_calls_hours']['id']  
        # Homesite
        case 22:
            sheet_name = 'Homesite Forecast'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'homesite'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['homesite_forecasted_calls_hours']['id']  
        # JPS     
        case 23:
            sheet_name = 'JPS MBJ'
            table_name = 'mbj_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'jps'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['jps_forecasted_calls_hours']['id']    
        case 24:
            sheet_name = 'JPS KGN'
            table_name = 'kgn_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'jps'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['jps_forecasted_calls_hours']['id']
        # Kroger
        case 25:
            sheet_name = 'Kroger SLU'
            table_name = 'slu_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 'client_billable_training_hours', 
                                'client_ancillary_revenue_usd']
            schema = 'kroger'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['kroger_forecasted_calls_hours']['id']    
        case 26:
            sheet_name = 'Kroger KGN'
            table_name = 'kgn_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 'client_billable_training_hours', 
                                'client_ancillary_revenue_usd']
            schema = 'kroger'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['kroger_forecasted_calls_hours']['id']   
        # Lifetouch
        case 27:
            sheet_name = 'Lifetouch SLU'
            table_name = 'slu_lifetouch_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'lifetouch_shutterfly'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['lifetouch_forecasted_calls_hours']['id']   
        case 28:
            sheet_name = 'Lifetouch KGN'
            table_name = 'kgn_lifetouch_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'lifetouch_shutterfly'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['lifetouch_forecasted_calls_hours']['id'] 
        # Liveperson geo
        case 29:
            sheet_name = 'GEO'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'liveperson'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['liveperson_forecasted_calls_hours']['id'] 
        # Louis Vuitton
        case 30:
            sheet_name = 'Louis Vuitton Forecast'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'louis_vuitton'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['louis_vuitton_forecasted_calls_hours']['id']
        # Maxsold
        case 31:
            sheet_name = 'Maxsold Forecast'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_developer_hours', 'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_developer_hours', 'client_ancillary_revenue_usd']
            schema = 'maxsold'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['maxsold_forecasted_calls_hours']['id']
        # Ministry of Health
        case 32:
            sheet_name = 'MOH Forecast'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
            'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 'client_billable_training_hours', 
            'client_ancillary_revenue_usd']
            schema = 'ministry_health'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['ministry_of_health_forecasted_calls_hours']['id']
        # Office Depot
        case 33:
            sheet_name = 'Office Depot GEO'
            table_name = 'geo_calls_and_hours_forecast'
            expected_columns = ["date","wfm_direct_billing","wfm_direct_chat","wfm_direct_english","wfm_direct_sms",
            "wfm_direct_spanish","wfm_direct_web_support","wfm_grand_and_toy","wfm_odpb_billing","wfm_odpb_chat",
            "wfm_odpb_chat_strategic","wfm_odpb_key_accounts","wfm_odpb_sms","wfm_odpb_spanish","wfm_odpb_strategic_support",
            "wfm_odpb_web_support","wfm_private_brand_hours","wfm_billable_training_hours","client_direct_billing","client_direct_chat",
            "client_direct_english","client_direct_sms","client_direct_spanish","client_direct_web_support",
            "client_grand_and_toy","client_odpb_billing","client_odpb_chat","client_odpb_chat_strategic",
            "client_odpb_key_accounts","client_odpb_sms","client_odpb_spanish","client_odpb_strategic_support",
            "client_odpb_web_support","client_private_brand_hours","client_billable_training_hours"]
            schema = 'office_depot'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['office_depot_forecasted_calls_hours']['id']
        case 34:
            sheet_name = 'Office Depot WAH'
            table_name = 'wah_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_strategic_calls', 'wfm_gat_hours', 'wfm_oss_hours', 
                                'wfm_billable_training_hours', 'client_strategic_calls', 'client_gat_hours', 
                                'client_oss_hours', 'client_billable_training_hours']
            schema = 'office_depot'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['office_depot_forecasted_calls_hours']['id']                                     
        # Ontellus
        case 35:
            sheet_name = 'Ontellus Forecast'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'ontellus'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['ontellus_forecasted_calls_hours']['id']
        # PSN
        case 36:
            sheet_name = 'PSN Forecast'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'psn'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['psn_forecasted_calls_hours']['id']
        # Run Buggy
        case 37:
            sheet_name = 'WAH'
            table_name = 'glb_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_csr_hours', 'wfm_billable_csr2_hours', 'wfm_billable_supervisor_hours', 'wfm_billable_sdr_usa_hours',
                                'wfm_billable_training_hours', 'wfm_ancillary_revenue_usd', 'client_billable_csr_hours', 
                                'client_billable_csr2_hours', 'client_billable_supervisor_hours', 'client_billable_sdr_usa_hours', 'client_billable_training_hours', 
                                'client_ancillary_revenue_usd']
            schema = 'run_buggy'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['run_buggy_forecasted_calls_hours']['id']
        # Shutterfly
        case 38:
            sheet_name = 'Shutterfly KGN'
            table_name = 'kgn_shutterfly_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'lifetouch_shutterfly'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['shutterfly_forecasted_calls_hours']['id']
        case 39:
            sheet_name = 'Shutterfly SLU'
            table_name = 'slu_shutterfly_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'lifetouch_shutterfly'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['shutterfly_forecasted_calls_hours']['id']  
        # Speedy
        case 40:
            sheet_name = 'Speedy MBJ'
            table_name = 'mbj_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'speedy'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['speedy_forecasted_calls_hours']['id']
        case 41:
            sheet_name = 'Speedy SLU'
            table_name = 'slu_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'speedy'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['speedy_forecasted_calls_hours']['id']
        # The General
        case 42:
            sheet_name = 'WAH'
            table_name = 'wah_customer_service_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue', 'client_billable_production_hours','client_billable_training_hours', 
                                'client_ancillary_revenue']
            schema = 'the_general'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['the_general_customer_service_forecasted_calls_hours']['id']
        case 43:
            sheet_name = 'BAH'
            table_name = 'bah_customer_service_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue', 'client_billable_production_hours','client_billable_training_hours', 
                                'client_ancillary_revenue']
            schema = 'the_general'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['the_general_customer_service_forecasted_calls_hours']['id']
        case 44:
            sheet_name = 'WAH'
            table_name = 'wah_blended_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue', 'client_billable_production_hours','client_billable_training_hours', 
                                'client_ancillary_revenue','wfm_billable_overtime_hours','client_billable_overtime_hours']
            schema = 'the_general'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['the_general_sales_forecasted_calls_hours']['id']
        #Active Engage
        case 45:
            sheet_name = 'GEO'
            table_name = 'geo_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 'client_billable_training_hours', 
                                'client_ancillary_revenue_usd']
            schema = 'active_engage'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['active_engage_forecasted_calls_hours']['id']                                                                               
        #IAA
        case 46:
            sheet_name = 'KGN'
            table_name = 'kgn_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_day_production_hours', 'wfm_billable_night_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_day_production_hours', 'client_billable_night_production_hours', 'client_billable_training_hours', 
                                'client_ancillary_revenue_usd']
            schema = 'iaa'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['iaa_forecasted_calls_hours']['id']
        #TDS Field Services
        case 47:
            sheet_name = 'MBJ'
            table_name = 'mbj_field_services_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_field_services_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_field_services_hours', 'client_billable_training_hours', 
                                'client_ancillary_revenue_usd']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_field_services_hours_and_calls_forecast']['id']
        #TDS Financial Services
        case 48:
            sheet_name = 'MBJ'
            table_name = 'mbj_financial_services_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_fin_services_tier_one_hours', 'wfm_billable_fin_services_tier_two_hours', 
                                'wfm_billable_training_hours', 'wfm_ancillary_revenue_usd', 'client_billable_fin_services_tier_one_hours', 
                                'client_billable_fin_services_tier_two_hours',  'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_financial_services_hours_and_calls_forecast']['id']
        case 49:
            sheet_name = 'SLU'
            table_name = 'slu_financial_services_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_fin_services_tier_one_hours', 'wfm_billable_fin_services_tier_two_hours', 
                                'wfm_billable_training_hours', 'wfm_ancillary_revenue_usd', 'client_billable_fin_services_tier_one_hours', 
                                'client_billable_fin_services_tier_two_hours',  'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_financial_services_hours_and_calls_forecast']['id']
        #TDS Repair
        case 50:
            sheet_name = 'MBJ'
            table_name = 'mbj_repair_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_consumer_hours','wfm_billable_commercial_hours','wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd','wfm_billable_daart_hours','wfm_billable_augmented_coach_hours','client_billable_consumer_hours','client_billable_commercial_hours', 'client_billable_training_hours', 
                                'client_ancillary_revenue_usd','client_billable_daart_hours','client_billable_augmented_coach_hours']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_repair_hours_and_calls_forecast']['id']
        case 51:
            sheet_name = 'SLU'
            table_name = 'slu_repair_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_consumer_hours','wfm_billable_commercial_hours','wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd','wfm_billable_daart_hours','wfm_billable_augmented_coach_hours','client_billable_consumer_hours','client_billable_commercial_hours', 'client_billable_training_hours', 
                                'client_ancillary_revenue_usd','client_billable_daart_hours','client_billable_augmented_coach_hours']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_repair_hours_and_calls_forecast']['id']            
        #TDS Sales
        case 52:
            sheet_name = 'MBJ'
            table_name = 'mbj_sales_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_sales_hours', 'wfm_billable_customer_service_hours', 
                                'wfm_billable_training_hours', 'wfm_ancillary_revenue_usd', 'client_billable_sales_hours', 
                                'client_billable_customer_service_hours',  'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_sales_hours_and_calls_forecast']['id']
        case 53:
            sheet_name = 'SLU'
            table_name = 'slu_sales_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_sales_hours', 'wfm_billable_customer_service_hours', 
                                'wfm_billable_training_hours', 'wfm_ancillary_revenue_usd', 'client_billable_sales_hours', 
                                'client_billable_customer_service_hours',  'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_sales_hours_and_calls_forecast']['id']
        case 54:
            sheet_name = 'MBJ'
            table_name = 'mbj_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'liveperson'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['liveperson_forecasted_calls_hours']['id']
        case 55:
            sheet_name = 'GEO'
            table_name = 'geo_calls_and_hours_forecast'
            expected_columns = ['date','wfm_billable_reservation_calls','wfm_billable_guest_assurance_calls',
                                'wfm_billable_diamond_calls','wfm_billable_customer_care_calls', 'wfm_billable_email',
                                'wfm_billable_training_hours','wfm_ancillary_revenue_usd',
                                'client_billable_reservation_calls','client_billable_guest_assurance_calls',
                                'client_billable_diamond_calls','client_billable_customer_care_calls', 'client_billable_email',
                                'client_billable_training_hours','client_ancillary_revenue_usd']
            schema = 'hilton'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['hilton_forecasted_calls_hours']['id']
        case 56:
            sheet_name = 'KGN'
            table_name = 'kgn_customer_service_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue', 'client_billable_production_hours','client_billable_training_hours', 
                                'client_ancillary_revenue','wfm_billable_overtime_hours','client_billable_overtime_hours']
            schema = 'the_general'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['the_general_customer_service_forecasted_calls_hours']['id']
        # 1800 flowers KGN
        case 57:
            sheet_name = 'KGN'
            table_name = 'kgn_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_mins', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_mins', 
                                'client_billable_training_hours', 'client_ancillary_revenue_usd']
            schema = 'one_eight_hundred_flowers'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['one_eight_hundred_flowers_forecasted_calls_hours']['id']            
        # Anyone Home BEL
        case 58:
            sheet_name = 'Anyone Home Belize'
            table_name = 'bze_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 'wfm_billable_wfm_hours',
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 'client_billable_training_hours', 
                                'client_billable_wfm_hours', 'client_ancillary_revenue_usd']
            schema = 'anyone_home'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['anyone_home_forecasted_calls_hours']['id']        
        case 59:
            sheet_name = 'TCC JLP Forecast'
            table_name = 'kgn_tcc_jlp_forecast_billable_hours'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 'client_billable_production_hours',
                                'client_billable_training_hours']
            schema = 'tcc_jlp'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tcc_jlp_hours_and_calls_forecast']['id']
        case 60:
            sheet_name = 'KGN'
            table_name = 'kgn_ccc_forecast_billable_hours'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_production_claim','wfm_billable_training_hours', 'client_billable_production_hours', 'client_billable_production_claim', 'client_billable_training_hours']
            schema = 'ccc'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['ccc_hours_and_calls_forecast']['id']
        case 61:
            sheet_name = 'KGN'
            table_name = 'kgn_mia_forecast_billable_hours'
            expected_columns = ['date','wfm_billable_concierge_hours','wfm_billable_concierge_training_hours',
                                'wfm_billable_sales_hours','wfm_billable_sales_training_hours','client_billable_concierge_hours',
                                'client_billable_concierge_training_hours','client_billable_sales_hours',
                                'client_billable_sales_training_hours',"wfm_billable_post_op_hours","wfm_billable_post_op_premiun_hours",
                                "wfm_billable_post_op_training_hours","client_billable_post_op_hours","client_billable_post_op_premiun_hours",
                                "client_billable_post_op_training_hours"]
            schema = 'mia'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['mia_hours_and_calls_forecast']['id']
        case 62:
            sheet_name = 'Kroger GEO'
            table_name = 'geo_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 'client_billable_training_hours', 
                                'client_ancillary_revenue_usd']
            schema = 'kroger'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['kroger_forecasted_calls_hours']['id']
        case 63:
            sheet_name = 'MBJ'
            table_name = 'mbj_com_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_field_services_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_field_services_hours', 'client_billable_training_hours', 
                                'client_ancillary_revenue_usd']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_com_hours_and_calls_forecast']['id']
        case 64:
            sheet_name = 'GEO Forecast'
            table_name = 'geo_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_inbound_billable_calls', 'wfm_outbound_billable_calls', 'wfm_billable_classroom_training_hours', 'wfm_ancillary_revenue_usd',
                                'client_inbound_billable_calls', 'client_outbound_billable_calls','client_billable_classroom_training_hours', 'client_ancillary_revenue_usd']
            schema = 'walmart'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['walmart_forecasted_calls_hours']['id'] 
        case 65:
            sheet_name = 'BZE'
            table_name = 'bze_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'client_billable_production_hours', 'client_billable_training_hours']
            schema = 'epremium'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['epremium_hours_and_calls_forecast']['id']
        case 66:
            sheet_name = 'Henry Schein One Forecast'
            table_name = 'sap_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_csr1_production_hours', 'wfm_billable_csr2_production_hours', 'wfm_billable_training_csr1_hours', 'wfm_billable_training_csr2_hours', 'client_billable_csr1_production_hours', 'client_billable_csr2_production_hours', 'client_billable_training_csr1_hours', 'client_billable_training_csr2_hours']
            schema = 'henry_schein'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['henry_schein_and_calls_forecast']['id']
        case 67:
            sheet_name = 'MBJ'
            table_name = 'mbj_calls_and_hours_forecast'
            expected_columns = ["date","wfm_billable_production_hours","wfm_billable_training_hours","client_billable_production_hours","client_billable_training_hours"]
            schema = 'auto_europe'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['auto_europe_hours_and_calls_forecast']['id']
        case 68:
            sheet_name = 'SLU'
            table_name = 'slu_calls_and_hours_forecast'
            expected_columns = ["date","wfm_billable_production_res_tier_one_calls", "wfm_billable_production_res_tier_two_calls", "wfm_billable_production_cus_calls",	
                                "wfm_billable_training_hours", "client_billable_production_res_tier_one_calls", "client_billable_production_res_tier_two_calls",	
                                "client_billable_production_cus_calls",	"client_billable_training_hours"]
            schema = 'avis'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['avis_hours_and_calls_forecast']['id']
        case 69:
            sheet_name = 'KGN'
            table_name = 'kgn_calls_and_hours_forecast'
            expected_columns = ["date","wfm_billable_production_res_tier_one_calls", "wfm_billable_production_res_tier_two_calls", "wfm_billable_production_cus_calls",	
                                "wfm_billable_training_hours", "client_billable_production_res_tier_one_calls", "client_billable_production_res_tier_two_calls",	
                                "client_billable_production_cus_calls",	"client_billable_training_hours"]
            schema = 'avis'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['avis_hours_and_calls_forecast']['id']
        case 70:
            sheet_name = 'KGN'
            table_name = 'kgn_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_production_hours', 'client_billable_training_hours', 
                                'client_ancillary_revenue_usd']
            schema = 'active_engage'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['active_engage_forecasted_calls_hours']['id']    
        case 71:
            sheet_name = 'Homesite KGN'
            table_name = 'kgn_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'client_billable_production_hours', 'client_billable_training_hours']
            schema = 'homesite'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['homesite_forecasted_calls_hours']['id']
        case 72:
            sheet_name = 'BZE'
            table_name = 'bze_mia_forecast_billable_hours'
            expected_columns = ['date','wfm_billable_production_hours','wfm_billable_training_hours','client_billable_production_hours','client_billable_training_hours']
            schema = 'mia'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['mia_hours_and_calls_forecast']['id']
        case 73:
            sheet_name = 'MBJ'
            table_name = 'mbj_cno_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_field_services_hours', 'wfm_billable_training_hours', 
                                'wfm_ancillary_revenue_usd', 'client_billable_field_services_hours', 'client_billable_training_hours', 
                                'client_ancillary_revenue_usd']
            schema = 'tds'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['tds_cno_hours_and_calls_forecast']['id']
        case 74:
            sheet_name = 'SLU'
            table_name = 'slu_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_sdr_stl_hours','wfm_billable_sdr_training_hours', 'client_billable_sdr_stl_hours','client_billable_sdr_training_hours']
            schema = 'run_buggy'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['run_buggy_forecasted_calls_hours']['id']
        case 75:
            sheet_name = 'SAP'
            table_name = 'sap_calls_and_hours_forecast'
            expected_columns = ["date","wfm_billable_production_hours","wfm_billable_training_hours","client_billable_production_hours","client_billable_training_hours"]
            schema = 'goals'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['goals_forecasted_calls_hours']['id']
        case 76:
            sheet_name = 'GEO'
            table_name = 'geo_calls_and_hours_forecast'
            expected_columns = ['date', 'wfm_billable_production_hours', 'wfm_billable_training_hours', 
                                'client_billable_production_hours', 'client_billable_training_hours']
            schema = 'epremium'
            file_id = utils.get_config('dshub_sharepoint_config')['files']['epremium_hours_and_calls_forecast']['id']
            
    print(f"Running script for {schema}.{table_name} from {sheet_name}")
    sheet_downloader_and_uploader(sheet_name, table_name, expected_columns, schema, file_id)
