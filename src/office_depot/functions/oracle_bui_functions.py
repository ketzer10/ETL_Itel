import pandas as pd
import numpy as np
import lxml.etree as ET
import re
import datetime
import io
from lxml import etree
from bs4 import BeautifulSoup
from utils.sharepoint_wrapper import get_sharepoint_file_by_id, ClientContext


def get_agent_name_from_email(email: str) -> str:
    """It extracts the agent's name from the email.

    Args:
        email (str): Agent's email. [first.last@domain.net]
    Returns:
        agent_name: Agent's name.
    """

    agent_name = " ".join(list(map(lambda x: x.capitalize(), (email.split("@")[0].split(".")))))
    return agent_name

def extract_date_from_file_name(file_name: str) -> datetime.date:
    """It extracts the date from the file's name.

    Args:
        file_name (str): File name.

    Returns:
        datetime.date: Date created.
    """
    str_date = file_name.split(" ")[-1].split(".")[0].split("_")
    month = int(str_date[0])
    day = int(str_date[1])
    year = int(str_date[2])
    date = datetime.date(year, month, day)
    
    return date

def extract_data(cell: str) -> str:
    """It extracts the values to be stored within a DataFrame.

    Args:
        cell (str): The cell's info from a xml file.

    Returns:
        str: Value to be stored within a DataFrame
    """
    pattern = r'<ss:Data ss:Type="Number">(\d+)</ss:Data>|<ss:Data ss:Type="String">(.+?)</ss:Data>'
    match = re.search(pattern, cell)
    return match.group(1) or match.group(2) if match else None

def create_df(all_files: list, ctx: ClientContext, skiprows: int, skip_last_rows: int, num_columns: int, extract_date_from_file_name_function: str) -> pd.DataFrame:
    all_dfs = []
    for file in all_files:
        file_name = file[0]
        file_id = file[2]
        dato = get_sharepoint_file_by_id(ctx, file_id)
        try:
            print(f"Creating a Dataframe with contents from file: '{file_name}'")
            data = dato["contents"].getvalue().decode('utf-8-sig')
            character = """\ufeff"""
            data = data.replace(character, "")
            soup = BeautifulSoup(data, "xml")
            cells = soup.findAll("Cell")
            if skip_last_rows:
                cells = cells[:-6]  # It deletes the last rows for reports which have no needed rows e.g, Total, Record count.
            info = list(map(lambda x: extract_data(str(x)), cells))
            info = info[skiprows:].copy()
            dicc_keys = info[:num_columns]
            dicc = {}
            for key in dicc_keys: dicc[key] = []
            dicc_loc = 0
            for cell in info[num_columns:]:
                if dicc_loc == num_columns: dicc_loc = 0
                dicc[dicc_keys[dicc_loc]].append(cell)
                dicc_loc += 1
            df = pd.DataFrame(dicc)
            if extract_date_from_file_name_function:
                df["Date"] = extract_date_from_file_name_function(file_name)
            all_dfs.append(df)
        except ValueError as e:
            print(f"It was not possible to create a Dataframe with this file: {e}")
    
    df = all_dfs[0] if len(all_dfs) == 1 else pd.concat(all_dfs, axis=0)

    return df