import utils.utils as utils
import utils.dbutils as dbutils
import utils.dfutils as dfutils
from io import StringIO
import os
import pandas as pd
from datetime import datetime as dt
import datetime
import utils.sharepoint_wrapper as shwp
import numpy as np

def file_sharepoint_upload(ctx, df, filename):
    file_buffer = StringIO()
    df.to_csv(path_or_buf = file_buffer, index = False)
    file_buffer.seek(0)
    df_file = file_buffer.getvalue().encode('utf-8')
    
    shwp.upload_file_to_sharepoint_folder(ctx, "2bb95ab7-e602-47c0-ab87-b38f41d19bb2", filename, df_file)

def validate_next_day_date(df, time_columns, time_in):
    print("Validating next day dates", time_columns)
    for column in time_columns:
        df[column] = df[column].astype('datetime64[ns]')
        df[column] = np.where(df[column] < df[time_in], df[column] + datetime.timedelta(days=1), df[column])

    return df

def format_time_columns(df, time_columns, time_format="%H:%M"):
    for column in time_columns:
        df[column] = pd.to_datetime(df[column])
        df[column] = df[column].dt.strftime(time_format)
    return df

def format_date_column(df, date_columns, date_format="%Y-%m-%d"):
    for column in date_columns:
        df[column] = pd.to_datetime(df[column])
        df[column] = df[column].dt.strftime(date_format)
    return df

def schedule_file_output(account_name: str, relevant_headers: str, folder_key: str):

    print('Getting SharePoint context.')
    ctx = shwp.get_datascience_hub_ctx()
    folder_id = utils.get_config('dshub_sharepoint_config')['folders'][folder_key]['id']
    folder_name = utils.get_config('dshub_sharepoint_config')['folders'][folder_key]['name']
    historical_folder_id = utils.get_config('dshub_sharepoint_config')['folders'][folder_key]['historical_id']

    print(f"Running script for {folder_key}: {folder_name}")       
    sorted_files_names_extensions_and_ids = shwp.get_files_names_extensiones_and_ids_by_folder_id(ctx, folder_id)

    file_ids = list(item[2] for item in sorted_files_names_extensions_and_ids)
    print("Files to load:", len(file_ids))

    accounts = {'WalmartSAP': 'WM', 'AnyoneHomeSAP': 'AOH', 'HenryScheineSAP': 'HSO'}

    output_path = r'C:\Users\David.Nolasco\Desktop\blobs\HRPlusSchedules\Final Pilot Honduras August 2023\\'

    query_hrmaster = 'SELECT legacy_id, national_id_number FROM hrmaster.employees WHERE country = \'Honduras\''
    query_hrplus = 'SELECT badge_number, national_id FROM hrplus.employees'

    conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
    cursor = conn.cursor()                                                                                   
    cursor.fast_executemany = True

    df_hrmaster = pd.read_sql_query(query_hrmaster, conn)
    df_hrmaster = dfutils.fill_dataframe_nulls(df_hrmaster)

    df_hrplus = pd.read_sql_query(query_hrplus, conn)
    df_hrplus = dfutils.fill_dataframe_nulls(df_hrplus)

    conn.close()

    df_merged = pd.merge(df_hrmaster, df_hrplus, 'left', left_on = 'national_id_number', right_on = 'national_id')
    df_merged['legacy_id'] = df_merged['legacy_id'].astype('str')
    df_merged['badge_number'] = df_merged['badge_number'].astype('str')    

    account = accounts[account_name]
    #final_path = folder_path + '\\' + account + '\\'
    for file_id in file_ids:
        file_obj = shwp.get_sharepoint_file_by_id(ctx, file_id) # Get the file from the SharePoint
        print('Reading', file_obj['file_name'])
        df_schedule = pd.read_excel(file_obj['contents']) # Read into a DataFrame
        if account != 'AOH':
            df_schedule.columns = relevant_headers
            df_schedule['date'] = df_schedule['date'].dt.date
            date_range = [((df_schedule['date']).min()).strftime('%Y%m%d'), ((df_schedule['date']).max()).strftime('%Y%m%d')] #Get date range for file name
            df_schedule['Employee ID'] = df_schedule['Employee ID'].astype('str') #Change type for merge
            df_schedule_output = pd.merge(left = df_schedule, right = df_merged, how = 'left', left_on = 'Employee ID', right_on = 'legacy_id') #Merge schedule file with employee IDs for mappings
            df_schedule_output = dfutils.fill_dataframe_nulls(df_schedule_output) 
            df_schedule_output.drop(columns='Employee ID', inplace = True) #Legacy ID, no longer needed at this point
            df_schedule_output.rename(columns={'badge_number':'Employee ID'}, inplace=True) # Rename to keep the badge number
            df_schedule_output = df_schedule_output[relevant_headers] # Keep only relevant headers
            df_schedule_output = validate_next_day_date(df_schedule_output, ['TimeOut', 'LunchStart', 'LunchEnd', 'Break 1 Start', 'Break 1 End', 'Break 2 Start', 'Break 2 End'], 'TimeIn')
            date_range = [((df_schedule_output['date']).min()).strftime('%Y%m%d'), ((df_schedule_output['date']).max()).strftime('%Y%m%d')] #Get date range for file name
            df_schedule_output = format_date_column(df_schedule_output, ['date'])
            df_schedule_output = format_time_columns(df_schedule_output, ['TimeIn','TimeOut', 'LunchStart', 'LunchEnd', 'Break 1 Start', 'Break 1 End', 'Break 2 Start', 'Break 2 End'])
            #df_schedule_output.to_csv(path_or_buf=output_path+'[ALL] ES_'+account_name+'_'+date_range[0]+'_'+date_range[1]+'.csv', index=False) # Ouput df to csv
        if account == 'AOH':
            df_schedule = pd.read_excel(file_obj['contents'], sheet_name='Schedules', skiprows=1) # Read Schedule Tab to df
            df_roster = pd.read_excel(file_obj['contents'], sheet_name='Roster', skiprows = 14) # Read Roster Tab to df
            df_roster = df_roster[['Community Name', 'Emp_ID']] # Keep relevant headers from roster
            df_schedule = pd.merge(left = df_schedule, right = df_roster, how='left', left_on='Community Name', right_on='Community Name') # Join dfs to get IDs
            df_schedule = df_schedule[df_schedule['Site'] == 'Honduras'] # Filter for Honduras only
            df_schedule['Emp_ID'] = df_schedule['Emp_ID'].astype('str')
            df_schedule = df_schedule[df_schedule.columns[[18,19,20,21,22,23,23,24,25]]] # Keep relevant columns. This is not great but these columns have headers with dates which would vary from file to file so the column numbers are used. Subsequently, local time schedules for the seven weekdays are kept, along with the added ID.
            df_schedule_output = pd.merge(left = df_schedule, right = df_merged, how = 'left', left_on = 'Emp_ID', right_on = 'legacy_id') # Merge schedules with IDs to map global ids
            df_schedule_output = pd.melt(df_schedule_output, id_vars = ["badge_number"], var_name = 'date', value_name='TimeIn') # Unpivot days to date-id attribute and Time
            df_schedule_output = df_schedule_output[df_schedule_output['date'].str.contains('_') == False] # Remove rows with underscore in the date attribute column. These would really only be the other columns that are not dates. 
            df_schedule_output = df_schedule_output[(df_schedule_output['TimeIn'].str.contains('-') == True) & (df_schedule_output['TimeIn'].str.contains(':') == True)] # Keep rows with a hyphen, these are schedule ranges. A colon can also be used to identify the time ranges. 
            df_schedule_output['date'] = df_schedule_output['date'].apply(lambda txt: txt.split(".")[0]) # Remove period number generated as a result of the schedules having EST schedules first when loaded to the df.    
            df_schedule_output[['day_name', 'day', 'month_name', 'year']] = df_schedule_output['date'].str.split(pat = ' ', expand = True) # Split in date components
            #df_schedule_output['month_name'] = dt.strptime(df_schedule_output['month_name'], r'%b').month # Format month
            df_schedule_output['month'] = pd.to_datetime(df_schedule_output['month_name'], format='%b').dt.month.astype('int8') # Make month an integer
            df_schedule_output['new_date'] = pd.to_datetime(df_schedule_output[['year', 'month', 'day']]) # Build date from integer components
            df_schedule_output['new_date'] = df_schedule_output['new_date'].astype("datetime64[ns]") # Set datatype 
            df_schedule_output = dfutils.fill_dataframe_nulls(df_schedule_output) # Fill nulls
            df_schedule_output.drop(columns='date', inplace = True)            
            df_schedule_output.rename(columns={'badge_number':'Employee ID', 'TimeIn':'FullSched', 'new_date':'date'}, inplace = True) # Rename column headers
            df_schedule_output[['TimeIn', 'TimeOut']] = (df_schedule_output['FullSched'].str.split(pat = '-', expand = True)) # Split schedule date range to TimeIn TimeOut values
            df_schedule_output['TimeIn'] = df_schedule_output['TimeIn'].str.strip()
            df_schedule_output['TimeOut'] = df_schedule_output['TimeOut'].str.strip()
            df_schedule_output['TimeIn'] = df_schedule_output['TimeIn'].str.replace(pat='0A', repl='0 A')
            df_schedule_output['TimeIn'] = df_schedule_output['TimeIn'].str.replace(pat='0P', repl='0 P')
            df_schedule_output['TimeOut'] = df_schedule_output['TimeOut'].str.replace(pat='0A', repl='0 A')
            df_schedule_output['TimeOut'] = df_schedule_output['TimeOut'].str.replace(pat='0P', repl='0 P')
            df_schedule_output = df_schedule_output[relevant_headers] # Keep relevant columns
            df_schedule_output['TimeIn'] = (df_schedule_output['TimeIn'].astype("datetime64")).dt.strftime("%H:%M") # Convert to datetime format
            df_schedule_output['TimeOut'] = (df_schedule_output['TimeOut'].astype("datetime64")).dt.strftime("%H:%M") # Convert to datetime format
            date_range = [((df_schedule_output['date']).min()).strftime('%Y%m%d'), ((df_schedule_output['date']).max()).strftime('%Y%m%d')] #Get date range for file name
        df_schedule_output.dropna(axis = 0, subset = ['TimeIn'], inplace=True) # Remove rows with no schedule
        df_schedule_output.dropna(axis = 0, subset = ['Employee ID'], inplace=True) # Remove rows with no employee id
        df_schedule_output.index
        
        df_schedule_output["Employee ID"] = df_schedule_output["Employee ID"].str.zfill(8)
        filename = 'ES_'+account_name+'_'+date_range[0]+'_'+date_range[1]+'.csv'        
        df_schedule_output.to_csv(path_or_buf=output_path+'ES_'+account_name+'_'+date_range[0]+'_'+date_range[1]+'.csv', index=False) # Ouput df to csv
        file_sharepoint_upload(ctx, df_schedule_output, filename)

        # Moving to Historical Folder
        print("Moving to Historical Folder")
        shwp.move_file_to_folder(ctx, historical_folder_id, file_id)
        print("Correctly moved to historical folder")

def main(optional: list):
    match optional[0]:
        case 0:
            relevant_headers = ['Employee ID', 'date', 'TimeIn', 'TimeOut', 'LunchStart', 'LunchEnd', 'Break 1 Start', 'Break 1 End', 'Break 2 Start', 'Break 2 End']
            account_name = 'WalmartSAP'
            folder_key = 'sap_walmart_schedules' 
        case 1:
            relevant_headers = ['Employee ID', 'date', 'TimeIn', 'TimeOut', 'LunchStart', 'LunchEnd', 'Break 1 Start', 'Break 1 End', 'Break 2 Start', 'Break 2 End']
            account_name = 'HenryScheineSAP'      
            folder_key = 'sap_henry_scheine_one_schedules'      
        case 2:
            relevant_headers = ['Employee ID', 'date', 'TimeIn', 'TimeOut']
            account_name = 'AnyoneHomeSAP' 
            folder_key = 'sap_anyone_home_schedules'

    schedule_file_output(account_name=account_name, relevant_headers=relevant_headers, folder_key=folder_key)