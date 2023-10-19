from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import utils.dbutils as dbutils
import src.anyone_home.community.community_utils as community_utils

def parse_html(html_content):
    """
    Parses an HTML file with
    """

    print('Loading HTML into BeautifulSoup constructor.')
    soup = BeautifulSoup(html_content, features='lxml')
    agent_list = soup.find('table', {"id":'ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_AgentReportGrid'})
    agent_list = agent_list.find('tbody', recursive=False)
    table_rows = agent_list.find_all("tr", recursive=False)

    print('Parsing HTML.')
    final_df = None
    # Iterate through each row which contains a table with the agent information
    for tr in table_rows:
        # Get the agent name. After the agent name the word "Schedule" can be found. Splits the string and strips the spaces.
        agent_name = tr.find('div', class_= 'wfmsg-export-table').text.split("Schedule")[0].strip()
        # Find the HTML table which contains the information
        data_table = tr.find('table', class_= 'wfmsg-table-view')
        # If the data table is not empty
        if data_table:
            # Read the data from the HTML table. read_html() returns a list of DataFrames. Since we only expect to find one DataFrame we just read one
            table = pd.read_html(str(data_table))[0]
            # Drop the last row of the table since it contains the subtotal 
            table.drop(table.tail(1).index, inplace=True)
            # Create a column with the agent name
            table['name'] = agent_name
            # If the final dataframe is None just create the dataframe, else append
            final_df = table if final_df is None else final_df.append(table)

    return final_df

def transform_dataframe(source_df: pd.DataFrame, location):

    # Drop columns and rename the remaining ones
    drop_cols = ['In Queue Variance %', 'Unnamed: 6', 'Out Queue Variance %', 'Unnamed: 11', 
             'Unnamed: 15', 'Non Scheduled / In Queue Hours', 'Total Adherence %']
    new_cols = ['date', 'transactions', 'scheduled_in_queue', 'actual_in_queue', 'in_queue_variance',
                'scheduled_out_queue', 'actual_out_queue', 'out_queue_variance', 'total_scheduled', 
                'total_variance', 'name']
    source_df.drop(columns=drop_cols, inplace=True)
    source_df.columns = new_cols

    # Convert to datetime. Date string is in the following format: Thursday, 23 December 2021
    source_df['date'] = pd.to_datetime(source_df['date'], format='%A, %d %B %Y').dt.date

    # Add location. Later used to safe delete the database
    source_df['location'] = location

    return source_df

def upload_dataframe(source_df: pd.DataFrame):
    print('Opening database connection.') 
    conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
    cursor = conn.cursor()                                                                                   
    cursor.fast_executemany = True
    # Upload to database
    dbutils.perform_safe_delete_insert_with_keys(conn, ['date', 'location'], source_df, 'anyone_home', 'glb_adherence')

    
def main(optional = None):
    # Creating a run mode for automatic and manual date selection. Automatic date selection selects today - n days.
    # manual mode takes in a start and an end date. Default mode is 0 (Automatic). Be careful when downloading too much data. Because:
    # 1. It takes too damn long to load and the wait time provided to the crawler might not be enough.
    mode = 1
    if mode == 0:
        # Downloads the data until yesterday and 3 days prior to that. Three days is not reasonable but this takes too long
        days_to_download = 2
        end_date = datetime.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=days_to_download)
    elif mode == 1:
        start_date = datetime(2022, 3, 14)
        end_date = datetime(2022, 3, 31)
    else:
        raise ValueError('Mode not supported')

    # Create a list of dates between start and end dates
    date_list  = pd.date_range(start_date, end_date, freq='d').tolist()

    # Get the URL for logging in
    login_url = community_utils.get_built_url('login')

    # The ID of the element to wait on to detect load.
    id_to_wait = '#ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_Table2'

    try: 
        # Iterate through the list. It is better to download one date at a time
        for date in date_list:
            # Format to pass to the URL
            formatted_start = date.strftime('%Y-%m-%d').replace('-', '%2f')
            formatted_end = date.strftime('%Y-%m-%d').replace('-', '%2f')

            # Run the code twice for each supervisor/country
            for i in range(2):
                sup_id = '1017' if i == 0 else '3'
                location = 'Honduras' if i == 0 else 'Guyana'
                
                params = {
                    'td=': formatted_start,
                    'fd=': formatted_end,
                    'sp=': sup_id
                }

                print(f'Downloading data for {location} on {date}.')
                adherence_url = community_utils.get_built_url('adherence', params)
                html_content = community_utils.get_community_html_content(login_url,  adherence_url, id_to_wait)
                result_df = parse_html(html_content)
                result_df = transform_dataframe(result_df, location)
                upload_dataframe(result_df)
                
    except Exception as e:
        print(e)