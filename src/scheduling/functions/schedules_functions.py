import utils.dfutils as dfutils
import pandas as pd
import numpy as np
import utils.dbutils as dbutils
import datetime
from io import StringIO
import utils.sharepoint_wrapper as shwp

def filter_rows_wrong(df) -> pd.DataFrame:
    

    info = pd.DataFrame({'error': [], 'records': [], 'date': [], 'lob': []})

    print("Removing Erroneous Rows")
    print(df.shape)
    total = df.shape[0]

    print("Shape before wrong row filter:", df.shape)    
    print("Removing Erroneous Rows")    

    count_breaks = int((df.columns.str.contains("Break").sum())/2)


    #df = df.dropna(how="any", subset=["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd"]) #Leaving in empty Lunches per HRPlus
    info = info.append({'error': 'Lunch times are missing','records': total - int(df.dropna(how="any", subset=["LunchStart","LunchEnd"]).shape[0])}, ignore_index=True)
    info = info.append({'error': 'TimeIn and TimeOut are erroneous','records': total - int(df.drop(df[df["TimeIn"] == df["TimeOut"]].index).shape[0])}, ignore_index=True)
    info = info.append({'error': 'LunchStart and LunchEnd are erroneous','records': total - int(df.drop(df[df["LunchStart"] == df["LunchEnd"]].index).shape[0])}, ignore_index=True)

    for i in range(count_breaks):
        df = df.drop(df[(df[f"Break {i+1} Start"] == df[f"Break {i+1} End"]) & (df[f"Break {i+1} Start"] != None) & (df[f"Break {i+1} End"] != None)].index)
    
    info = info.append({'error': 'Breaks are erroneous', 'records': total - df.shape[0]}, ignore_index=True)

    df = df.dropna(how="any", subset=["Employee ID","date","TimeIn","TimeOut"])
    df = df.drop(df[df["TimeIn"] == df["TimeOut"]].index)
    df = df.drop(df[df["LunchStart"] == df["LunchEnd"]].index)

    print("Output after wrong row filter:", df.shape)

    return [df,info]

def convert_time_to_datetime(df, time_columns, date_column):
    print("Converting to datetime columns", time_columns)
    for column in time_columns:
        df[column] = df[date_column] + " " + df[column]

    return df

def validate_next_day_date(df, time_columns, time_in):
    print("Validating next day dates", time_columns)
    for column in time_columns:
        df[column] = np.where(df[column] < df[time_in], df[column] + datetime.timedelta(days=1), df[column])

    return df

def processed_file_mover(files, historical_folder_id, ctx):
    for file in files:
        print("Moving to Historical Folder")
        shwp.move_file_to_folder(ctx, historical_folder_id, file)
        print("Correctly moved to historical folder")  

def output_file(df, lob, output_folder_id, ctx):
    try:
        folder_obj = ctx.web.get_folder_by_id(output_folder_id)
        ctx.load(folder_obj).execute_query()

        folder_obj_url = folder_obj.properties['ServerRelativeUrl'] 

        start_date = min(df["date"].astype("datetime64").dt.strftime("%Y%m%d"))
        end_date = max(df["date"].astype("datetime64").dt.strftime("%Y%m%d"))
        print("Date range:", start_date, " to", end_date)
        output_file_name = "ES_" + lob + "_" + start_date + "_" + end_date + ".csv"  

        file_buffer = StringIO()    
        df.to_csv(path_or_buf = file_buffer, index = False)
        file_buffer.seek(0)
        df_file = file_buffer.getvalue().encode('utf-8')

        print("Writing file: ", folder_obj_url, "/", output_file_name)
        folder_obj.upload_file(output_file_name, df_file).execute_query()
        
    except Exception as e:
        print(e)

def file_dates_output(df, lob):
    df["file"] = lob   

def file_combiner(file_indices, file_min_date, file_max_date, files_read, lob, output_folder_id, successful_file_ids, historical_folder_id, ctx):
    attributes = {"index":file_indices, "min_date": file_min_date, "max_date": file_max_date}
    files_df = pd.DataFrame(data=attributes)
    sorted_df = files_df.sort_values(["max_date", "min_date"], ascending=[False, False])
    file_dates_output(sorted_df, lob)
    print(sorted_df)
    stack_order = sorted_df["index"].to_list()
    ordered_files = [files_read[i] for i in stack_order]

    processed_dates = []
    output_df = ordered_files[0]
    for file in ordered_files:    
        dates_in_file = (file["date"].drop_duplicates()).to_list()
        print("Dates in file:", dates_in_file)    
        append_df = file[~file["date"].isin(processed_dates)]
        print("DF size:", file.size, "\nAppend size:", append_df.size)
        new_dates = (append_df["date"].drop_duplicates()).to_list()
        processed_dates.extend(new_dates)
        print("Dates to add:", new_dates)
        output_df = pd.concat([output_df, append_df])
        print("------------------------------------")
        
    print("Dates in final file:", (output_df["date"].drop_duplicates()).to_list())
    output_df = output_df.sort_values(["date"])
    output_df = output_df.drop_duplicates()
    output_file(output_df, lob, output_folder_id, ctx)
    #processed_file_mover(successful_file_ids, historical_folder_id, ctx)    

def site_filter(df, client, site):
    print("Filtering", client, "for", site)
    match client:
        case "TDSFinancialServices":
            df = df[df["site"] == site]
            df = df.drop(columns=["site"])
        case "TDSRepair":
            df = df[df["site"] == site]
            df = df.drop(columns=["site"])
        case "TDSSales":
            df = df[df["site"] == site]
            df = df.drop(columns=["site"])        
        case "TDSFieldServices":
            df = df[df["site"] == site]
            df = df.drop(columns=["site"])                   
        case "Altice":
            df = df.replace(to_replace = ["Vieux Fort", "Montego Bay", "Kingston"], value = ["SLU", "MBJ", "KGN"])
            df = df[df["Site"] == site]
            df = df.drop(columns=["Site"])
        case "Hilton":            
            df = df[df["Site"] == site]
            #df = df.drop(columns="Site", inplace=True)            
    return df

def mappings_tds_id() -> pd.DataFrame:
    conn = dbutils.open_connection_with_scripting_account()
    df = pd.read_sql_query("SELECT hrm_id, tds_id, site FROM itel_datasi.tds.hrm_employee_id;", con=conn)
    return df

def format_time_columns(df, time_columns, time_format):
    for column in time_columns:
        df[column] = df[column].dt.strftime(time_format)
    return df

def format_date_column(df, date_columns, date_format):
    for column in date_columns:
        df[column] = df[column].dt.strftime(date_format)
    return df

def transforms_function_slu_hilton_schedules(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df = df[["HRM_ID", "Nominal Date", "Start", "Stop", "Site", "Code"]]

    df = df[df["Site"] == "SLU"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format="%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    code_remap_start= info_transform_function["code_remap_start"]
    code_remap_end = info_transform_function["code_remap_end"]

    index_columns = ["date", "Employee ID"]

    start_code_row_filter = list(code_remap_start.keys())
    print("Codes for schedules:", start_code_row_filter)
    df =  df[df["Code"].isin(start_code_row_filter)]
    df_start = df.drop(columns = ["Stop"])
    df_end = df.drop(columns = ["Start"])

    for codes in code_remap_start.items():
        df_start = df_start.replace(codes[0], codes[1])    

    for codes in code_remap_end.items():
        df_end = df_end.replace(codes[0], codes[1])
    
    print("Pivoting on", index_columns)
    df_pivot_start = pd.pivot(df_start, index = index_columns, columns = "Code", values = "Start").reset_index()
    df_pivot_end = pd.pivot(df_end, index = index_columns, columns = "Code", values = "Stop").reset_index()
    df_pivot_merged = df_pivot_start.merge(right = df_pivot_end, how = "left", on = index_columns).rename_axis(None, axis=1)
    print("Merged", df_pivot_start.columns.to_list(), "with", df_pivot_end.columns.to_list(), "on", index_columns)

    df = df_pivot_merged[info_transform_function["output_columns"]]

    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = convert_time_to_datetime(df, time_columns=output_time_columns, date_column="date")
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)

    df,info = filter_rows_wrong(df)

    return [df,info]

def transforms_function_mbj_hilton_schedules(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df = df[["HRM_ID", "Nominal Date", "Start", "Stop", "Site", "Code"]]

    df = df[df["Site"] == "MBJ"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format="%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    code_remap_start= info_transform_function["code_remap_start"]
    code_remap_end = info_transform_function["code_remap_end"]

    index_columns = ["date", "Employee ID"]

    start_code_row_filter = list(code_remap_start.keys())
    print("Codes for schedules:", start_code_row_filter)
    df =  df[df["Code"].isin(start_code_row_filter)]
    df_start = df.drop(columns = ["Stop"])
    df_end = df.drop(columns = ["Start"])

    for codes in code_remap_start.items():
        df_start = df_start.replace(codes[0], codes[1])    

    for codes in code_remap_end.items():
        df_end = df_end.replace(codes[0], codes[1])
    
    print("Pivoting on", index_columns)
    df_pivot_start = pd.pivot(df_start, index = index_columns, columns = "Code", values = "Start").reset_index()
    df_pivot_end = pd.pivot(df_end, index = index_columns, columns = "Code", values = "Stop").reset_index()
    df_pivot_merged = df_pivot_start.merge(right = df_pivot_end, how = "left", on = index_columns).rename_axis(None, axis=1)
    print("Merged", df_pivot_start.columns.to_list(), "with", df_pivot_end.columns.to_list(), "on", index_columns)

    df = df_pivot_merged[info_transform_function["output_columns"]]


    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = convert_time_to_datetime(df, time_columns=output_time_columns, date_column="date")
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)

    df,info = filter_rows_wrong(df)


    return [df,info]

def transforms_function_kgn_hilton_schedules(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df = df[["HRM_ID", "Nominal Date", "Start", "Stop", "Site", "Code"]]

    df = df[df["Site"] == "KGN"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format="%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    code_remap_start= info_transform_function["code_remap_start"]
    code_remap_end = info_transform_function["code_remap_end"]

    index_columns = ["date", "Employee ID"]

    start_code_row_filter = list(code_remap_start.keys())
    print("Codes for schedules:", start_code_row_filter)
    df =  df[df["Code"].isin(start_code_row_filter)]
    df_start = df.drop(columns = ["Stop"])
    df_end = df.drop(columns = ["Start"])

    for codes in code_remap_start.items():
        df_start = df_start.replace(codes[0], codes[1])    

    for codes in code_remap_end.items():
        df_end = df_end.replace(codes[0], codes[1])
    
    print("Pivoting on", index_columns)
    df_pivot_start = pd.pivot(df_start, index = index_columns, columns = "Code", values = "Start").reset_index()
    df_pivot_end = pd.pivot(df_end, index = index_columns, columns = "Code", values = "Stop").reset_index()
    df_pivot_merged = df_pivot_start.merge(right = df_pivot_end, how = "left", on = index_columns).rename_axis(None, axis=1)
    print("Merged", df_pivot_start.columns.to_list(), "with", df_pivot_end.columns.to_list(), "on", index_columns)

    df = df_pivot_merged[info_transform_function["output_columns"]]

    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = convert_time_to_datetime(df, time_columns=output_time_columns, date_column="date")
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)  

    df,info = filter_rows_wrong(df)

    return [df,info]

def transforms_function_slu_altice_schedules(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df = df[["HRM", "Nominal Date", "Start", "Stop", "Code"]]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    df = df.dropna(thresh=5)
    df = df.drop_duplicates(subset=["Employee ID","date","Code"])

    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format="%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)

    code_remap_start = info_transform_function["code_remap_start"]
    code_remap_end = info_transform_function["code_remap_end"]

    index_columns = ["Employee ID","date"]

    start_code_row_filter = list(code_remap_start.keys())
    print("Codes for schedules:", start_code_row_filter)
    df =  df[df["Code"].isin(start_code_row_filter)]
    
    df_start = df.drop(columns = ["Stop"])
    df_end = df.drop(columns = ["Start"])

    for codes in code_remap_start.items():
        df_start = df_start.replace(codes[0], codes[1])    

    for codes in code_remap_end.items():
        df_end = df_end.replace(codes[0], codes[1])

    print("Pivoting on", index_columns)

    df_pivot_start = pd.pivot(df_start, index = index_columns, columns = "Code", values = "Start").reset_index()
    df_pivot_end = pd.pivot(df_end, index = index_columns, columns = "Code", values = "Stop").reset_index()

    df_pivot_merged = df_pivot_start.merge(right = df_pivot_end, how = "left", on = index_columns).rename_axis(None, axis=1)
    print("Merged", df_pivot_start.columns.to_list(), "with", df_pivot_end.columns.to_list(), "on", index_columns)

    df = df_pivot_merged[info_transform_function["output_columns"]]

    df,info = filter_rows_wrong(df)

    return [df,info]

def transforms_function_slu_kroger_schedules(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"]  

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    df = df.dropna(thresh=10)

    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)

    df = df[info_transform_function["output_columns"]]
    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = convert_time_to_datetime(df, time_columns=output_time_columns, date_column="date")
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)    

    df,info = filter_rows_wrong(df)

    return [df,info]

def transforms_function_kgn_ancestry_schedules(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Unnamed: 0","Employee ID","date","Unnamed: 3","Unnamed: 4","Unnamed: 5","Code","Start","Unnamed: 8","Unnamed: 9","Stop"]
    df = df[["Employee ID","date","Code","Start","Stop"]]
    df = df.dropna(subset=["Employee ID","Code"], how="all")
    df[["Employee ID","date"]] = df[["Employee ID","date"]].ffill(axis=0)
    df["Employee ID"] = df["Employee ID"].apply(lambda x: str(x).split(" ")[1])
    df = df.dropna(subset=["Code","Start","Stop"], how="all").reset_index(drop=True)

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M:%S"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format="%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)

    interval = True
    code_breaks = 1
    timein = ''

    # Rename, Replace -> Codes
    for index, row in df.iterrows():
            if index != 0 and row["date"] != df.loc[index-1,"date"]: 
                interval = True
                code_breaks = 1
                df = df.append({'Employee ID': df.loc[index-1,"Employee ID"], 
                                'date':df.loc[index-1,"date"], 
                                'Code':'SHIFT',
                                'Start':timein,
                                'Stop':df.loc[index-1,"Stop"]}, ignore_index=True)
            if "Break" in row["Code"]:
                df.loc[index,'Code'] = f"Break {code_breaks}"
                code_breaks+=1
            if interval:
                timein = row["Start"]

            interval = False

    codes = ["Lunch","Break 1","Break 2","Break 3","Break 4","SHIFT"]
    df = df[df["Code"].isin(codes)]

    df = df.drop_duplicates(subset=["Employee ID","date","Code"])

    index_columns = ["Employee ID","date"]

    df_start = df.drop(columns = ["Stop"])
    df_end = df.drop(columns = ["Start"])

    print("Pivoting on", index_columns)

    df_pivot_start = pd.pivot(df_start, index = index_columns, columns = "Code", values = "Start").reset_index()
    df_pivot_end = pd.pivot(df_end, index = index_columns, columns = "Code", values = "Stop").reset_index()

    df_pivot_merged = df_pivot_start.merge(right = df_pivot_end, how = "left", on = index_columns, suffixes=(' Start',' End')).rename_axis(None, axis=1)
    print("Merged", df_pivot_start.columns.to_list(), "with", df_pivot_end.columns.to_list(), "on", index_columns)

    df_pivot_merged = df_pivot_merged.rename(columns = {'SHIFT Start':'TimeIn', 
                                                        'SHIFT End':'TimeOut', 
                                                        'Lunch Start':'LunchStart',
                                                        'Lunch End':'LunchEnd'})

    df = df_pivot_merged[info_transform_function["output_columns"]]

    df,info = filter_rows_wrong(df)

    return [df,info]

def transforms_function_tds(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df = df.loc[:,~df.columns.str.startswith('Unnamed')]
    df = df[["Activity", "Start", "End"]]
    df = df[df["Activity"].str.contains("Organization|Daily") == False]

    df["Employee ID"] = df[df["Activity"].str.contains("Employee") == True]['Activity']
    df[["Employee ID"]] = df[["Employee ID"]].ffill(axis=0)
    df["Employee ID"] = df["Employee ID"].apply(lambda x: str(x).split(" ")[1] if "Employee" in str(x) else x)
    df["date"] = df[df["Activity"].str.contains("Date") == True]['Activity']
    df[["date"]] = df[["date"]].ffill(axis=0)
    df["date"] = df["date"].apply(lambda x: str(x).replace("Date: ","").strip())

    df = df[df["Activity"].str.contains("Employee|Date") == False]

    additional = ["Loss Additional Hours","Lost Additional Hours BPO","Make-up Time", "Make-up Time BPO", "Make-up Time ITEL", "Overtime Break", "Overtime Gap", "Overtime Lunch", "Overtime Phone", "Project (Direct) Overtime", "Project Overtime", "Shift/Overtime Gap", "X- Lost of additional hours"]
    df = df[~df["Activity"].isin(additional)].reset_index(drop=True)

    interval = True
    code_breaks = 1
    timein = ''

    # Rename, Replace -> Codes
    for index, row in df.iterrows():
            if index != 0 and row["date"] != df.loc[index-1,"date"]: 
                interval = True
                code_breaks = 1
                df = df.append({'Employee ID': df.loc[index-1,"Employee ID"], 
                                'date':df.loc[index-1,"date"], 
                                'Activity':'SHIFT',
                                'Start':timein,
                                'End':df.loc[index-1,"End"]}, ignore_index=True)
            if "Break" in row["Activity"]:
                df.loc[index,'Activity'] = f"Break {code_breaks}"
                code_breaks+=1
            if interval:
                timein = row["Start"]

            interval = False
            

    codes = ["Lunch","Break 1","Break 2","SHIFT"]
    df = df[df["Activity"].isin(codes)]

    print("Final headers", df.columns)
    
    
    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M:%S"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format="%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)   

    df = df.drop_duplicates(subset=["Employee ID","date","Code"])

    index_columns = ["Employee ID","date"]
    
    df_start = df.drop(columns = ["Stop"])
    df_end = df.drop(columns = ["Start"])
    
    print("Pivoting on", index_columns)

    df_pivot_start = pd.pivot(df_start, index = index_columns, columns = "Code", values = "Start").reset_index()
    df_pivot_end = pd.pivot(df_end, index = index_columns, columns = "Code", values = "Stop").reset_index()

    df_pivot_merged = df_pivot_start.merge(right = df_pivot_end, how = "left", on = index_columns, suffixes=(' Start',' End')).rename_axis(None, axis=1)
    print("Merged", df_pivot_start.columns.to_list(), "with", df_pivot_end.columns.to_list(), "on", index_columns)

    df_pivot_merged = df_pivot_merged.rename(columns = {'SHIFT Start':'TimeIn', 
                                                        'SHIFT End':'TimeOut', 
                                                        'Lunch Start':'LunchStart',
                                                        'Lunch End':'LunchEnd'})

    df = df_pivot_merged[info_transform_function["output_columns"]]

    df = pd.merge(df,mappings_tds_id(), how="left", left_on=["Employee ID"], right_on=["tds_id"])
    df["Employee ID"] = df["hrm_id"]

    df = df.drop(columns=['hrm_id', 'tds_id'])

    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"

    df = convert_time_to_datetime(df, time_columns=output_time_columns, date_column="date")
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)

    df,info = filter_rows_wrong(df)

    return [df,info]

def transforms_function_mbj_1800_flowers(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%Y-%m-%d %H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End", "Break 3 Start","Break 3 End"]
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    df,info = filter_rows_wrong(df)

    return [df,info]

def transforms_function_slu_speedy(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%Y-%m-%d %H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End", "Break 3 Start","Break 3 End"]
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")    

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    df,info = filter_rows_wrong(df)

    return [df,info]   

def transforms_function_mbj_speedy(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%Y-%m-%d %H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End", "Break 3 Start","Break 3 End"]
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    df,info = filter_rows_wrong(df)

    return [df,info]

def transforms_function_mbj_activengage(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame:    
    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    df,info = filter_rows_wrong(df)

    return [df,info]

def transforms_function_mbj_psn(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame:    
    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = convert_time_to_datetime(df, time_columns=output_time_columns, date_column="date")
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)

    df,info = filter_rows_wrong(df)

    return [df,info]


def transforms_function_kgn_iaa(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%Y-%m-%d %H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)

    df,info = filter_rows_wrong(df)

    return [df,info]

def transforms_function_mbj_ontellus(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%Y-%m-%d %H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)

    df,info = filter_rows_wrong(df)


    return [df,info]

def transforms_function_mbj_moh(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M:%S"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    print(df.head())
    df = convert_time_to_datetime(df, time_columns=output_time_columns, date_column="date")
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)  

    df,info = filter_rows_wrong(df)

    return [df,info]    

def transforms_function_mbj_breville(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    df,info = filter_rows_wrong(df)

    return [df,info]

def transforms_function_mbj_car8(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 
    df.columns = ["","Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"]
    df = df[["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"]]
    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    df,info = filter_rows_wrong(df)

    return [df,info]           

def transforms_function_mbj_jps(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%Y-%m-%d %H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]
    
    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)

    df,info = filter_rows_wrong(df)

    return [df,info]

def transforms_function_kgn_jps(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%Y-%m-%d %H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)
    df = filter_rows_wrong(df)

    df,info = filter_rows_wrong(df)

    return [df,info]

def transforms_function_kgn_kroger_schedules(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"]  

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    df = df.dropna(thresh=10)

    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M:%S"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)

    df = df[info_transform_function["output_columns"]]

    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = convert_time_to_datetime(df, time_columns=output_time_columns, date_column="date")
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)

    df,info = filter_rows_wrong(df)

    return [df,info]   

def transforms_function_kgn_tgcs(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%Y-%m-%d %H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]
    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)

    df,info = filter_rows_wrong(df)

    return [df,info]
    return df

def transforms_function_kgn_mia_aesthetics(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 
    df.columns = df.columns.str.replace(" ", "")
    df = df[['HRMID','Date','StartTime','EndTime','Break1Start','Break1End','LunchStart','LunchEnd','Break2Start','Break2End']]
    print("Removed name", df.columns.tolist())
    df.columns = ["Employee ID","date", "TimeIn","TimeOut","Break 1 Start","Break 1 End","LunchStart","LunchEnd","Break 2 Start","Break 2 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    df = filter_rows_wrong(df)

    return df

def transforms_function_kgn_1800_flowers(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    df.columns = ["Employee ID","date","TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%Y-%m-%d %H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]
    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)
    df = filter_rows_wrong(df)

    return df    


def transforms_function_kgn_lifetouch(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 
    df = df[["Date", "Employee ID", "Time In", "Time Out", "BreakStart", "Break End", "LunchStart", "lunch End", "Break2 Start", "Break End.1"]]
    df.columns = ["date", "Employee ID", "TimeIn","TimeOut","Break 1 Start","Break 1 End","LunchStart","LunchEnd","Break 2 Start","Break 2 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    df = filter_rows_wrong(df)

    return df

def transforms_function_kgn_shutterfly(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 
    df = df[["Date", "Employee ID", "Time In", "Time Out", "BreakStart", "Break End", "LunchStart", "Lunch End", "Break 2 Start", "Break 2 End"]]
    df.columns = ["date", "Employee ID", "TimeIn","TimeOut","Break 1 Start","Break 1 End","LunchStart","LunchEnd","Break 2 Start","Break 2 End"]
    df = df[df["TimeIn"] != "--:--"]
    print(df.head())
    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    print(df.head())
    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]

    df = filter_rows_wrong(df)

    return df

def transforms_function_mbj_liveperson(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 
    df = df[["Emp.ID","Date","Start","End","Break 1 Start","Break 1 Stop","Lunch Start","Lunch Stop","Break 2 Start","Break 2 Stop"]]
    df.columns = ["Employee ID","date","TimeIn","TimeOut","Break 1 Start","Break 1 End","LunchStart","LunchEnd","Break 2 Start","Break 2 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%Y-%m-%d %H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]
    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)
    df = filter_rows_wrong(df)

    return df

def transforms_function_kgn_walmart(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 
    df = df[["Emp. ID","Date","Start","End","Break 1 Start","Break 1 Stop","Lunch Start","Lunch Stop","Break 2 Start","Break 2 Stop"]]
    df.columns = ["Employee ID","date","TimeIn","TimeOut","Break 1 Start","Break 1 End","LunchStart","LunchEnd","Break 2 Start","Break 2 End"]

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    rows_before_clearing_empty = len(df)
    df = df.dropna(thresh=10)
    rows_after_clearing_empty = len(df)

    print("Dropped", rows_before_clearing_empty-rows_after_clearing_empty, "rows.")    
    
    time_columns = info_transform_function["df_handling"]["validate_datetime_columns"]["columns"]
    time_format = "%Y-%m-%d %H:%M"

    date_columns = info_transform_function["df_handling"]["validate_date_columns"]["columns"]
    date_format = "%Y-%m-%d"

    df = format_time_columns(df, time_columns, time_format)
    print("Formatted time", time_format)

    df = format_date_column(df, date_columns, date_format)
    print("Formatted date", date_format)
    
    df = df[info_transform_function["output_columns"]]
    output_time_columns = ["TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"]
    output_time_format = "%Y-%m-%d %H:%M"
    
    df = dfutils.validate_datetime_columns(df, columns = output_time_columns, date_format=output_time_format)    
    df = validate_next_day_date(df, time_columns=output_time_columns, time_in = "TimeIn")
    df = format_time_columns(df, time_columns=output_time_columns, time_format=output_time_format)
    df = filter_rows_wrong(df)

    return df    
