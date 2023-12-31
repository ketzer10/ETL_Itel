import json
import uuid
import jwt
import requests
import io
import time
import pyodbc
import pandas as pd
import utils.utils as utils
import utils.dbutils as dbutils
from datetime import date, datetime, timedelta


# AUTHENTICATION
def authenticating_talkdesk(credentials: json, account_name: str) -> str:
    """It uses the credentials contained in the "credentials" variable to authenticate with talkdesk API.
    
    Args:
        credentials: json load
        account_name (str): Name of the account to be used in the talkdesk API.
    
    Returns:
        access_token (str): An str which is a string to be used to download many reports from the API.
    """
    
    print("Authenticating client credentials...")
    # Client Private Key
    CLIENT_PRIVATE_KEY = credentials["private_key"]
    CLIENT_PRIVATE_KEY = "-----BEGIN PRIVATE KEY-----\n" + CLIENT_PRIVATE_KEY + "\n-----END PRIVATE KEY-----"
    # JWT Headers
    headers = {"kid": credentials["key_id"]}
    # JWT Payload
    payload = {"iss": credentials["id"],\
        "sub": credentials["id"],\
        "aud": f"https://{account_name}.talkdeskid.com/oauth/token",\
        "jti": str(uuid.uuid4()),\
        "exp": datetime.utcnow() + \
        timedelta(seconds=700),\
        "iat": datetime.utcnow()
    }
    # Signed JWT 
    jwt_token = jwt.encode(payload, CLIENT_PRIVATE_KEY, algorithm = credentials["algorithm"], headers = headers)
    payload = {
        "grant_type" : "client_credentials",
        "client_assertion_type":"urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
        "client_assertion":jwt_token
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }
    url = f"https://{account_name}.talkdeskid.com/oauth/token"
    print("Requesting access token...")
    response = requests.post(url, data=payload, headers=headers)
    response_json = json.loads(response.text)
    access_token = response_json["access_token"]
    print("Access Token obtained!")
    return access_token
    
# Execute the report
def execute_report(access_token: str, report_name: str, from_date: str, to_date: str) -> str:
    """It generates the Job ID which is a requirement to download reports from the talkesk API.

    Args:
        access_token (str): The access_token generated by the authenticating_talkdesk function.
        report_name (str): Name of the report to be downloaded from the talkdesk API (i.e studio_flow_execution, calls).
        from_date (str): Initial date of the registers contained in the desired report (yyyy-mm-dd).
        to_date (str): Final date of the registers contained in the desired report (yyyy-mm-dd).
    Returns:
        job_ib (str): This is going to be used to check the status of the requested report.
    """
    
    url = f"https://api.talkdeskapp.com/data/reports/{report_name}/jobs"
    payload = {
        "format": "csv",
        # "timezone": "America/Jamaica",
        "timespan": {
            "from": f"{from_date}T05:00:00+00:00",
            "to": f"{to_date}T04:59:59+00:00"
        }
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Executing {report_name} report for {from_date}T05:00:00+00:00 to {to_date}T04:59:59+00:00...")
    print(f"Getting Job ID...")
    response_json = json.loads(response.text)
    job_id = response_json["job"]["id"]
    print("Job ID was obtained!")
    
    return job_id

# Check the report's status
def check_report_status(access_token: str, report_name: str, job_id: str) -> bool:
    """It check the status of the requested report.

    Args:
        access_token (str): The access_token generated by the authenticating_talkdesk function.
        report_name (str): Name of the report to be downloaded from the talkdesk API (i.e studio_flow_execution, calls).
        job_id (str): This is going to be used to check the status of the requested report.

    Returns:
        bool: True if response from the API is "200", False if else.
    """
    
    url = f"https://api.talkdeskapp.com/data/reports/{report_name}/files/{job_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    result = str(response).split()[1][1:4]  # "<Report [###]>" -- After split: "[###]>" -- To check: "###" == "200"
    
    return True if result == "200" else False

# Check the report's status until created
def check_loop(access_token: str, report_name: str, job_id: str) -> bool:
    """This is a helper function to check many times the status of the report.

    Args:
        access_token (str): The access_token generated by the authenticating_talkdesk function.
        report_name (str): Name of the report to be downloaded from the talkdesk API (i.e studio_flow_execution, calls).
        job_id (str): This is going to be used to check the status of the requested report.

    Returns:
        bool:
    """
    
    print("Checking status report...")
    counter = 0
    time.sleep(5)
    while True:
        created = check_report_status(access_token, report_name, job_id)
        if created:
            print("The report was created!")
            return True
        else:
            print("The report is still not created. Take it easy, please.")
            counter += 1
            time.sleep(10)
        if counter == 10:
            return False
            
# Download the report
def download_report(access_token: str, report_name: str, job_id: str) -> json:
    url = f"https://api.talkdeskapp.com/data/reports/{report_name}/files/{job_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    
    return response

# Delete the report
def delete_report(access_token: str, report_name: str, job_id: str) -> json:
    url = f"https://api.talkdeskapp.com/data/reports/{report_name}/files/{job_id}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.delete(url, headers=headers)
    result = str(response).split()[1][1:4]  # "<Report [###]>" -- After split: "[###]>" -- To check: "###" == "200"
    print("The report was succesfully deleted! (API)") if result == "204" else print("It was not possible to delete the report :(")

# Create a Pandas DataFrame with the report's info
def create_df(response) -> pd.DataFrame:
    data = io.StringIO(response.text)
    df = pd.read_csv(data, sep=",")
    
    return df

def check_max_date_and_generate_dates_list_and_conn(table_name: str):
    print("Opening database connection with scripting account...")
    conn = dbutils.open_connection_with_scripting_account()
    cursor = conn.cursor()
    print(f"Checking MAX date from {table_name}")
    query = f"SELECT MAX(CAST(started_at_utc AS date)) FROM jps.{table_name}"
    cursor.execute(query)
    row = cursor.fetchone()
    max_date = row[0]
    print(f"MAX date from {table_name} is {max_date} UTC Timezone")
    today = date.today()
    delta = today - max_date
    dates_list = [str(max_date + timedelta(days=i)) for i in range(delta.days + 1)]
    
    return dates_list, conn

def generate_contacts_data(min_date, max_date) -> pd.DataFrame:
    conn = dbutils.open_connection_with_scripting_account()
    cursor = conn.cursor()
    print(f"Selecting Contacts calls data from '{min_date} 05:00:00' to '{max_date} 04:59:00'")
    query = f"""SELECT interaction_id, direction, contact_type, started_at_utc
                        FROM jps.talkdesk_calls_contacts
                        WHERE started_at_utc >= '{min_date} 05:00:00'
                        AND started_at_utc <= '{max_date} 04:59:00'"""
    
    contacts = pd.read_sql(query, conn)
    
    return contacts