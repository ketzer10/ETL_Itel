import gspread
import pandas as pd
import numpy as np
from utils.utils import get_decrypted_credential 
import ast

def get_gsheet_ctx() -> gspread.client.Client:
    credentials = get_decrypted_credential(["decryption_key"], "google_sheet_credentials")
    credentials["credential_dict"] = ast.literal_eval(credentials["credential_dict"])
    try:
        ctx = gspread.service_account_from_dict(credentials["credential_dict"])
    except Exception as e:
        raise Exception(f"Could not fetch Google Sheet context {e}")
    return ctx

def get_gsheet_file_by_id(ctx: gspread.client.Client, file_id: str) -> gspread.spreadsheet.Spreadsheet:
    try :
        sheet = ctx.open_by_key(file_id)
    except Exception as e:
        raise Exception(f"Could not fetch Google Sheet file {e}")
    return sheet

def get_gsheet_file_by_url(ctx, url: str) -> gspread.spreadsheet.Spreadsheet:
    try :
        sheet = ctx.open_by_url(url)
    except Exception as e:
        raise Exception(f"Could not fetch Google Sheet file {e}")
    return sheet
    
def get_gsheet_worksheets( file_obj: gspread.spreadsheet.Spreadsheet, tabs: list, head: int) -> list:
    worksheets = []
    worksheets_names = []
    try:
        for tab in tabs: 
            worksheet = file_obj.worksheet(tab)
            worksheet_name = worksheet.title
            worksheet = pd.DataFrame(worksheet.get_all_records(default_blank = np.nan, head = head))
            if worksheet.empty == False:
                worksheets.append(worksheet)
                worksheets_names.append(worksheet_name)
    except Exception as e:
        raise Exception(f"Couldn't get worksheets {e}")
    
    return worksheets, worksheets_names

def get_gsheet_worksheets_ignore( file_obj: gspread.spreadsheet.Spreadsheet, tabs_ignore: list, head: int) -> list:
    worksheets = []
    worksheets_names = []
    tabs = file_obj.worksheets()
    try:
        for tab in tabs:
            if tab.title not in tabs_ignore:
                worksheet_name = tab.title
                worksheet = pd.DataFrame(tab.get_all_records(default_blank = np.nan, head = head))
                if worksheet.empty == False:
                    worksheets.append(worksheet)
                    worksheets_names.append(worksheet_name)
    except Exception as e:
        raise Exception(f"Couldn't get worksheets {e}")
    
    return worksheets, worksheets_names

# libraries functions for handling worksheets and grand worksheet
def pass_function_worksheets(worksheets, worksheets_names):
    pass


def pass_function_grand_worksheet(grand_worksheet):
    pass


def handling_worksheets_add_source_tab_column(worksheets, worksheets_names):
    for i in range(len(worksheets)):
        worksheets[i]["source_tab"] = worksheets_names[i]