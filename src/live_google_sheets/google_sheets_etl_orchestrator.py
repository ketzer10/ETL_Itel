""" 
Downloads an Google Sheet file from Drive (Dev account) and uploads to the database.  
"""

from email import message
import utils.dbutils as dbutils
import pandas as pd
import utils.utils as utils
import utils.dfutils as dfutils
import utils.google_sheet_wrapper as gshw
import src.live_google_sheets.handling_functions_lib as handling_functions


def sheet_downloader_and_uploader(file_id: str, information_extract_worksheets: dict, handling_worksheets, expected_columns_for_stack: list, handling_grand_worksheet, grand_sheet_handling_todo: dict, schema: str, table_name: str):
    """Truncates and uploads a forecast live Excel files to the database. 
    Args: 
        table_name (str): The name of the table to upload to. 
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        file_id (str): ID for the file in sharepoint 
        worksheets_names (list): The names list of Google Sheet 
    """  
    
    
    # Getting the file from the Google Sheet and a list with all worksheets in dataframe object
    print("Getting Google Sheet context")
    ctx = gshw.get_gsheet_ctx()
    print("Getting file from Google Sheet site")    
    gsheet = gshw.get_gsheet_file_by_id(ctx, file_id)
    print("Getting worksheets from Sheet")
    for key in information_extract_worksheets["method"].keys():
        if key == "ignore_worksheets":
            worksheets, worksheets_names = gshw.get_gsheet_worksheets_ignore(
                gsheet, 
                information_extract_worksheets["method"]["ignore_worksheets"], 
                head = information_extract_worksheets["head"]
            ) 
        elif key == "extract_worksheets":
            worksheets, worksheets_names = gshw.get_gsheet_worksheets(
                gsheet, 
                information_extract_worksheets["method"]["extract_worksheets"], 
                head = information_extract_worksheets["head"]
            ) 
        else:
            raise Exception("Method to extract worksheets has not been specify")
    
    if len(worksheets) == 0:        
        return "Worksheet to read is empty."

    print("Handling worksheets")
    handling_worksheets(worksheets, worksheets_names)

    print("Stack the worksheets and getting the grand worsheet")
    grand_worksheet = dfutils.stack_dfs(worksheets, expected_columns_for_stack)
    
    # Handling a grand worksheet as dataframes
    print("Handling grand worksheet")
    handling_grand_worksheet(grand_worksheet)
    grand_worksheet = dfutils.df_handling(grand_worksheet, grand_sheet_handling_todo)
    
    # Fill empty values with NULLS 
    grand_worksheet = dfutils.fill_dataframe_nulls(grand_worksheet, '')

    #Load dataset into database
    print('Opening database connection')
    conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
    
    #Truncate and insert into the database
    print('Truncating database and reinserting.')    
    dbutils.perform_safe_truncate_insert(grand_worksheet, conn, schema, table_name)

    return "Worksheet read and uploaded successfully."

def main(optional: list):
    """ Runs the sheet_downloader_and_uploader.
    Args:
        optional (int): Run mode. 
    """

    match optional[0]:
        # Walmart          
        case 1:
            sheet_name = "Walmart Honduras Training Manual Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        case 2:
            sheet_name = "Walmart Honduras Operations Manual Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        # Anyone
        case 3:
            sheet_name = "Anyone Home Honduras Operations Manual Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        case 4:
            sheet_name = "Anyone Home Honduras Training Manual Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        # medical leaves
        case 5:
            sheet_name = "Honduras Medical Leaves" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        # Anyone Home Guyana Training
        case 6:
            sheet_name = "Anyone Home Guyana Training Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        # Liveperson
        case 7:
            sheet_name = "Liveperson Guyana Training Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        #Office Depot BPO 
        case 8:
            sheet_name = "Office Depot BPO Guyana Training Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        #Office Depot WAH 
        case 9:
            sheet_name = "Office Depot WAH Training Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]  
        #Maxsold 
        case 10:
            sheet_name = "Maxsold Training Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]    
        case 11:
            sheet_name = "Maxsold Operations Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]              
        #Activengage 
        case 12:
            sheet_name = "ActivEngage Training Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        case 13:
            sheet_name = "ActivEngage Operations Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        # Office Depot Mappings    
        case 14:
            sheet_name = "Office Depot Mappings" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]  
        # Liveperson Mappings    
        case 15:
            sheet_name = "Liveperson Mappings" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        # Anyone Home Mappings    
        case 16:
            sheet_name = "Anyone Home Mappings" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name] 
        # OD BPO Exceptions    
        case 17:
            sheet_name = "Office Depot BPO Exceptions" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]     
        # Liveperson Exceptions    
        case 18:
            sheet_name = "Liveperson Exceptions" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        # Anyone Home Exceptions    
        case 19:
            sheet_name = "Anyone Home Exceptions" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        # SAP Queries    
        case 20:
            sheet_name = "Honduras Payroll Queries" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        # SAP Bonuses
        case 21:
            sheet_name = "Honduras Bonuses" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        #Hilton 
        case 22:
            sheet_name = "Hilton Training Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        case 23:
            sheet_name = "Hilton Operations Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]            
        case 24:
            sheet_name = "Office Depot QA 2022"     
            print(sheet_name)      
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name] 
        case 25:
            sheet_name = "Walmart Exceptions"     
            print(sheet_name)      
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        # Henry Schein
        case 26:
            sheet_name = "Henry Schein Honduras Operations Manual Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        case 27:
            sheet_name = "Henry Schein Honduras Training Manual Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name] 
        #WM GEO 
        case 28:
            sheet_name = "Walmart Training Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        #H&D GEO 
        case 29:
            sheet_name = "Harry and David Operations Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        #Kroger GEO 
        case 30:
            sheet_name = "Kroger Operations Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]  
        #H&D GEO Training 
        case 31:
            sheet_name = "Harry and David Training Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        #Kroger GEO Training 
        case 32:
            sheet_name = "Kroger Training Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]                                    
        # GOALS          
        case 33:
            sheet_name = "GOALS Honduras Training Manual Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
        case 34:
            sheet_name = "GOALS Honduras Operations Manual Tracker" 
            print(sheet_name)
            config = utils.get_config_py("google_sheet_config_py")["files"][sheet_name]
    file_id = config["information_file"]["file_id"]
    information_extract_worksheets = config["information_extract_worksheets"] 
    handling_worksheets = config["handling_worksheets"]
    expected_columns_for_stack = config["expected_columns_for_stack"]
    handling_grand_worksheet = config["handling_grand_worksheet"]
    grand_sheet_handling_todo = config["grand_sheet_handling_todo"]
    schema = config["information_save_db"]["schema"]
    table_name = config["information_save_db"]["table_name"]
        
    message = sheet_downloader_and_uploader(file_id, information_extract_worksheets, handling_worksheets, expected_columns_for_stack, handling_grand_worksheet, grand_sheet_handling_todo, schema, table_name)
    print(message)
    print("========")