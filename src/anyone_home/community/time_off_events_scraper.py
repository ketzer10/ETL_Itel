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
    soup = BeautifulSoup(html_content, features="lxml")

    table = soup.find_all("table",
                          id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_EventList")[0].findAll('tr')

    result_data = []
    print('Parsing HTML.')
    for row in table:
        data = row.find_all('td')
        if len(data) >= 4:
            result_data.append([data[3].text.strip(), data[4].text.strip(), data[5].text.strip(),
                                data[6].text.strip()])

    result_data = pd.DataFrame(result_data, columns = ['agent_name', 'event_type', 'datetime', 'duration'])
    return result_data

def transform_dataframe(source_df: pd.DataFrame, location):
    print('Transforming DataFrame.')
    # Convert the duration column to float 
    source_df['duration'] = source_df['duration'].astype(float)

    # Convert the date_time column to datetime object instead of object
    source_df['datetime'] =  pd.to_datetime(source_df['datetime'], format='%d %b %Y %H:%M:%S %p')

    # Create new column with only date
    source_df['date'] = source_df['datetime'].dt.date

    # Create a location column and fill it with Honduras or Guyana. This is later used for the safe delete.
    source_df['location'] = location

    return source_df

def upload_dataframe(source_df: pd.DataFrame):
    print('Opening database connection.') 
    conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
    cursor = conn.cursor()                                                                                   
    cursor.fast_executemany = True
    # Upload to database
    dbutils.perform_safe_delete_insert_with_keys(conn, ['date', 'location'], source_df, 'anyone_home', 'glb_time_off_events')

    
def main(optional = None):
    # Creating a run mode for automatic and manual date selection. Automatic date selection selects today - n days.
    # manual mode takes in a start and an end date. Default mode is 0 (Automatic). Be careful when downloading too much data. Because:
    # 1. It takes too damn long to load and the wait time provided to the crawler might not be enough.
    # 2. The number of records in the HTML is fixed at 1,000,000 which is a ridiculous amount of data but you can break it if you abuse it.
    # If you want to abuse it anyhow you can just change the 1,000,000 to something (more) ridiculous anyway... It is the p parameter in the URL.
    mode = 1

    if mode == 0:
        # Downloads the data until yesterday and 5 days prior to that. Five days seems to be reasonable
        days_to_download = 5
        end_date = datetime.today() - timedelta(days=1)
        start_date = end_date - timedelta(days=days_to_download)
    elif mode == 1:
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2022, 1, 31)
    else:
        raise ValueError('Mode not supported')

    # Format to pass to the URL
    formatted_start = start_date.strftime('%Y-%m-%d').replace('-', '%2f')
    formatted_end = end_date.strftime('%Y-%m-%d').replace('-', '%2f')

    login_url = community_utils.get_built_url('login')
    id_to_wait = '#ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolder1_EventList'
    
    try: 
        # Run the script twice to download Guyana and Honduras. They have to be downloaded separately because they are under
        # different supervisor IDs. We can download all at the same time but we would download US agents which sucks tbh.
        supervisors = [['1017', 'Honduras'], ['3', 'Guyana'], ['1772' , 'Guyana']]
        for sup in supervisors:
            # Honduras

            params = {
                'fdate=': formatted_start,
                'tdate=': formatted_end,
                'sid=': sup[0]
            }

            time_off_events_url = community_utils.get_built_url('time_off_events', params)
            print(f'Downloading data for supervisor ID {sup[0]} in {sup[1]} between the dates {str(start_date)} and {str(end_date)}')
            html_content = community_utils.get_community_html_content(login_url,  time_off_events_url, id_to_wait)
            result_df = parse_html(html_content)
            result_df = transform_dataframe(result_df, sup[1])
            upload_dataframe(result_df)
    except Exception as e:
        print(e)


