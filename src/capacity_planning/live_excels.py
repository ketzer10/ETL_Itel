import utils.dbutils as dbutils
import pandas as pd
import utils.sharepoint_wrapper as shwp
import utils.utils as utils
import utils.dfutils as dfutils
from src.capacity_planning.config.config_files import configs

def sheet_downloader_and_uploader(file_id: str, sheet_name: str, read_with_dtype: dict, expected_columns: list, transform_function, info_transform_function: str, schema: str, table_name: str):
    """Truncates and uploads a forecast live Excel files to the database. 
    Args:
        sheet_name (str): The name of the sheet on the file to be uploaded.  
        table_name (str): The name of the table to upload to. 
        expected_columns (list): The list of columns for the sheet.
        schema (str): Schema in database where the table belongs.
        file_id (str): ID for the file in sharepoint
    """
    print("Getting SharePoint context.")
    ctx = shwp.get_datascience_hub_ctx()
    print("Opening database connection.") # Get Data Science Hub SharePoint context
    conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
    print("Getting file from SharePoint site.")    
    file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
    print("Loading Excel file into pandas DataFrame.")
    df = pd.read_excel(file_obj["contents"], sheet_name=sheet_name, dtype = read_with_dtype) # Read into a DataFrame

    # Verify that expected columns match the actual dataframe columns
    # assert expected_columns == df.columns.tolist(), "Expected columns do not match actual dataframe columns"

    # Fill empty values with NULLS 
    df = transform_function(df, info_transform_function)
    df = dfutils.fill_dataframe_nulls(df, "", "-")

    print(df)
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
            FILE_KEY = "planned_training_template"
            transform_function = configs[FILE_KEY]["transform_function"]
            info_transform_function = configs[FILE_KEY]["info_transform_function"]
            read_with_dtype = configs[FILE_KEY]["read_with_dtype"]
            sheet_name = "Fill Data"
            schema = "capacity_planning"
            table_name = "glb_planned_classes"
            expected_columns = [
                "Alignment",
                "Class Status",
                "STATUS",
                "ACCOUNT",
                "BATCH #",
                "FTE Target",
                "HTD",
                "Showed",
                "Fill %",
                "Show %",
                "Start Date",
                "OJT Date",
                "Roster Submit",
                "Site",
                "ACCOUNT2",
                "RD",
                "Manual"
            ]
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["planned_training_template"]["id"]

        case 2:
            FILE_KEY = "consolidated_cap_plan_new_details"
            transform_function = configs[FILE_KEY]["transform_function"]
            info_transform_function = configs[FILE_KEY]["info_transform_function"]
            read_with_dtype = configs[FILE_KEY]["read_with_dtype"]
            sheet_name = "New Details"
            schema = "capacity_planning"
            table_name = "glb_details"
            expected_columns = [
                    "Unnamed: 0",
                    "Id",
                    "business units",
                    "Site",
                    "Date ",
                    "Shrink",
                    "Attr",
                    "Training Attr",
                    "Pre Planned Training HC",
                    "Pre Planned Training category",
                    "Actual headcount -HC",
                    "Actual headcount-attr",
                    "OJT Headcount",
                    "OJT - FTE",
                    "Production FTE-required",
                    "Production FTE",
                    "Production FTE2-O/U",
                    "Production HC-required",
                    "Production HC-planned",
                    "Production HC-O/U",
                    "Reduction attrition",
                    "Reduction moves",
                    "OM -required",
                    "OM -planned",
                    "OM-O/U",
                    "Supervisors-required",
                    "Supervisors-planned",
                    "Supervisors-O/U",
                    "RTA-required",
                    "RTA-planned",
                    "RTA-O/U",
                    "WFA-required",
                    "WFA-planned",
                    "WFA-O/U",
                    "QA- required",
                    "QA-planned",
                    "QA-O/U",
                    "Trainers-required",
                    "Trainers-planned",
                    "Trainers-O/U",
                    "Required Seats WAH",
                    "Required Seats KGN",
                    "Required Seats UWI\n",
                    "Required Seats KGN BOT",
                    "Required Seats MBJ",
                    "Required Seats Chalmers",
                    "Required Seats SLU\n",
                    "Required Seats BAH",
                    "Required Seats GUY",
                    "Required Seats HON\n",
                    "Required Seats JEF",
                    "Seating In-Use WAH",
                    "Seating In-Use KGN",
                    "Seating In-Use UWI\n",
                    "Seating In-Use KGN BOT",
                    "Seating In-Use MBJ",
                    "Seating In-Use Chalmers",
                    "Seating In-Use SLU\n",
                    "Seating In-Use BAH",
                    "Seating In-Use GUY",
                    "Seating In-Use HON\n",
                    "Seating In-Use JEF",
                    "TSeats Available WAH",
                    "TSeats Available KGN",
                    "TSeats Available UWI",
                    "TSeats Available KGN BOT",
                    "TSeats Available MBJ",
                    "TSeats Available Chalmers",
                    "TSeats Available SLU",
                    "TSeats Available BAH",
                    "TSeats Available GUY",
                    "TSeats Available HON",
                    "TSeats Available JEF",
                    "Total PCs Available WAH",
                    "Total PCs Available KGN",
                    "Total PCs Available UWI",
                    "Total PCs Available KGN BOT",
                    "Total PCs Available MBJ",
                    "Total PCs Available Chalmers",
                    "Total PCs Available SLU",
                    "Total PCs Available BAH",
                    "Total PCs Available GUY",
                    "Total PCs Available HON",
                    "Total PCs Available JEF",
                    "RSeats vs APCs WAH",
                    "RSeats vs APCs KGN",
                    "RSeats vs APCs UWI",
                    "RSeats vs APCs KGN BOT",
                    "RSeats vs APCs MBJ",
                    "RSeats vs APCs Chalmers",
                    "RSeats vs APCs SLU",
                    "RSeats vs APCs BAH",
                    "RSeats vs APCs GUY",
                    "RSeats vs APCs HON",
                    "RSeats vs APCs JEF",
                    "RSeats from scheduling WAH\n",
                    "RSeats from scheduling KGN",
                    "RSeats from scheduling UWI\n",
                    "RSeats from scheduling KGN BOT",
                    "RSeats from scheduling MBJ",
                    "RSeats from scheduling Chalmers",
                    "RSeats from scheduling SLU",
                    "RSeats from scheduling BAH",
                    "RSeats from scheduling GUY",
                    "RSeats from scheduling HON",
                    "RSeats from scheduling JEF",
                    "Total PC Var2",
                    "Occupancy"
                ]
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["consolidated_cap_plan"]["id"]
        case 3:
            FILE_KEY = "consolidated_cap_plan_hiring_details"
            transform_function = configs[FILE_KEY]["transform_function"]
            info_transform_function = configs[FILE_KEY]["info_transform_function"]
            read_with_dtype = configs[FILE_KEY]["read_with_dtype"]
            sheet_name = "Hiring Details"
            schema = "capacity_planning"
            table_name = "glb_hiring_details"
            expected_columns = []
            file_id = utils.get_config("dshub_sharepoint_config")["files"]["consolidated_cap_plan"]["id"]
        
    print(f"Running script for {schema}.{table_name} from {sheet_name}")
    sheet_downloader_and_uploader(file_id, sheet_name, read_with_dtype, expected_columns, transform_function, info_transform_function, schema, table_name)