import utils.dfutils as dfutils
import pandas as pd
import numpy as np
import utils.dbutils as dbutils
import datetime
import utils.sharepoint_wrapper as shwp

def employee_transforms(df, case_config):
    # Transform dataframe
    df = dfutils.change_dataframe_columns_name(df, case_config["rename_cols"])   
    df = dfutils.validate_date_columns(df, case_config["date_cols"], date_format="%Y-%m-%d")
    for date_column in case_config["date_cols"]:
        print("Formatting:", date_column)
        df[date_column] = pd.to_datetime(df[date_column]).dt.date    
          

    text_columns = ["global_id", "last_name", "first_name", "other_name", "fulltime_parttime", "drivers_permit", 
                    "pno", "status_in_position", "empltype_code", "unit_code", "preferred_name", "home_telephone", 
                    "sex", "phone_extension", "marital_status", "statustype_code", "inland_revenue_id", "national_insurance_id", 
                    "national_id", "first_passport_no", "second_passport_no", "salutation", "religion_code", "nationality_code", 
                    "shift_worker", "address_line_one", "address_line_two", "address_line_three", "prior_name", "disability", 
                    "requisition_no", "hired_by", "hire_reason", "hire_source", "adj_hire_reason", "fax_number", "badge_number", 
                    "empl_class"]

    df = dfutils.validate_text_columns(df, text_columns)                          
    df = dfutils.fill_dataframe_nulls(df)
    for column in text_columns:
        df[column] = df[column].str.slice(0,448)  

    return df

def timesheet_transform(df, case_config):
    # Transform dataframe
    conn = dbutils.open_connection_with_scripting_account()
    cursor = conn.cursor()
    query = "SELECT MAX(dayWorked) FROM hrplus.time_sheet WHERE is_archived = 1"
    try:
        cursor.execute(query)
        row = cursor.fetchone()
        max_tsheet_arc_date = row[0]
        cursor.close()
        conn.close()
    except ValueError as e:
        print(e)
    # Transform dataframe


    df = dfutils.validate_date_columns(df, case_config["date_cols"], date_format="%Y-%m-%d")
    df = df[df.dayWorked.dt.date > max_tsheet_arc_date].copy()
    df = dfutils.fill_dataframe_nulls(df)
    #df = dfutils.validate_date_columns(df, case_config["date_cols"], date_format="%m/%d/%Y")
    for date_column in case_config["date_cols"]:
        print("Formatting:", date_column)
        df[date_column] = pd.to_datetime(df[date_column]).dt.date    
    
    # df = dfutils.validate_datetime_columns(df, case_config["time_cols"], date_format="%H:%M")
    df = dfutils.validate_datetime_columns(df, case_config["time_cols"], date_format="%H:%M:%S.%f")
    df = dfutils.fill_dataframe_nulls(df)
    for time_column in case_config["time_cols"]:
        print("Formatting:", time_column)
        df[time_column] = pd.to_datetime(df[time_column]).dt.time   


    #df.dropna("rows", 'any', subset=['dayWorked'],inplace=True)
    

          

    text_columns = ["timesheetId", "pay_group",  "callOut", "shift_Code", "projectCode", 
                    "projectPhaseCode", "ConditionCode", "ReasonCode", "User_Code"]
    df = dfutils.validate_text_columns(df, text_columns)   
    df = dfutils.fill_dataframe_nulls(df)
    int_cols = ["cycle_no", "pay_year", "approved", "paytype_rate", "shift_type"]   
    df = dfutils.validate_int_columns(df, int_cols)                       
    df = dfutils.fill_dataframe_nulls(df)
    for column in text_columns:
        df[column] = df[column].str.slice(0,447)  
    df = dfutils.fill_dataframe_nulls(df)
    df["is_archived"] = 0
    print(df)
    
    return df

def timesheet_arc_transform(df, case_config):
    # Transform dataframe
    conn = dbutils.open_connection_with_scripting_account()
    cursor = conn.cursor()
    query = "SELECT MAX(dayWorked) FROM hrplus.time_sheet WHERE is_archived = 1"
    try:
        cursor.execute(query)
        row = cursor.fetchone()
        max_tsheet_arc_date = row[0]
        cursor.close()
        conn.close()
    except ValueError as e:
        print(e)
    code_columns = ["ConditionCode", "ReasonCode", "User_Code"]
    for column in code_columns:
        try:
            df[column] = df[column].str.strip()
        except ValueError as e:
            print(f"It was not possible to strip the values for the {column}: {e}")
    
    df = dfutils.validate_date_columns(df, case_config["date_cols"], date_format="%Y-%m-%d")
    df = df[df.dayWorked.dt.date >= max_tsheet_arc_date].copy()
    df = dfutils.fill_dataframe_nulls(df)
    #df = dfutils.validate_date_columns(df, case_config["date_cols"], date_format="%m/%d/%Y")
    for date_column in case_config["date_cols"]:
        print("Formatting:", date_column)
        df[date_column] = pd.to_datetime(df[date_column]).dt.date
    
    df["is_archived"] = 1
    print(df)
    
    return df

def position_transforms(df, case_config):
    # Transform dataframe
    df = dfutils.change_dataframe_columns_name(df, case_config["rename_cols"])   
    df = dfutils.validate_date_columns(df, case_config["date_cols"], date_format="%Y-%m-%d")
    for date_column in case_config["date_cols"]:
        print("Formatting:", date_column)
        df[date_column] = pd.to_datetime(df[date_column]).dt.date    
     

    text_columns = ["pno", "stafftype_code", "job_code", "div_code", "div_name", "dept_code", "dept_name", 
                    "section_code", "section_name", "comp_code", "comp_name", "loc_code", "approved_by", 
                    "date_created", "statustype_code", "comments", "full_time", "executive", "pay_group"]

    df = dfutils.validate_text_columns(df, text_columns)                          
    df = dfutils.fill_dataframe_nulls(df)
    
    for column in text_columns:
        df[column] = df[column].str.slice(0,448)  

    return df

def empemail_transforms(df, case_config):
    df = dfutils.change_dataframe_columns_name(df, case_config["rename_cols"])
    int_cols = ["counter", "primaryemailaddress", "useprimaryemail", "workemailaddress"]
    df = dfutils.validate_int_columns(df, int_cols) 
    text_cols = ["empl_id", "address", "pager", "mobile", "personalmobile1", "personalmobile2", "companymobile"]
    df = dfutils.validate_text_columns(df, text_cols)
    df = dfutils.fill_dataframe_nulls(df)
    
    return df

def hriusers_transforms(df, case_config):
    df["Email"] = df.Email.astype(str)
    df = dfutils.change_dataframe_columns_name(df, case_config["rename_cols"])
    df = dfutils.fill_dataframe_nulls(df)
    df = dfutils.validate_date_columns(df, case_config["date_cols"], date_format="%Y-%m-%d")
    df = dfutils.fill_dataframe_nulls(df)
    
    return df

def reportsto_transforms(df, case_config):
    pno_columns = ["PNo", "Reportsto_PNo"]
    for column in pno_columns:
        df[column] = df[column].str.replace(r"\\x0a", "", regex=True)
        
    df["Supervisor_Type"] = df["Supervisor_Type"].str.replace(r"\\x0a", "nan", regex=True)
    df = dfutils.change_dataframe_columns_name(df, case_config["rename_cols"])
    df = dfutils.fill_dataframe_nulls(df)
    
    return df