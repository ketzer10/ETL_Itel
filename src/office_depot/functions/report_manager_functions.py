import utils.dfutils as dfutils
import pandas as pd
import numpy as np
import utils.dbutils as dbutils
import datetime
from io import StringIO
import utils.sharepoint_wrapper as shwp
import utils.dfutils as dfutils
def forecast_actuals_transform(df, info_transform_function):     

    df = df[["FcstName3", "SDate2", "PostedCalls3", "Textbox19", "LockedCalls4", "Textbox36", "Textbox37", 
             "Textbox63", "PostedHead3", "Textbox44", "LockedHead2", "Textbox21", "ActualTm5", "Textbox27", 
             "ActualHead4", "ActualHead6", "ActualAbnAll2"]]
             
    df.columns = info_transform_function["output_columns"]
    df.dropna(subset = ["channel"],inplace = True)
    df.drop_duplicates(["channel", "date"], inplace = True)
    df["date"] = df["date"].astype("datetime64[ns]")

    df = dfutils.df_handling(df, info_transform_function["df_handling"])    
    df = dfutils.fill_dataframe_nulls(df)

    return df

def office_depot_external_qa(df, info_transform_function, lob):
    ### RELEVANT LISTS
    original_headers=['PreName','SiteName','Reviewer','SDate','Textbox36','SessionID','Textbox16','QuestionSection1','PointsEarned1','PointsEarned2','QuestionText','Answer','PointsEarned','PointsPossibleDisplay','Textbox2']
    final_columns=['PreName','SiteName','Reviewer', 'SDate','Textbox36','SessionID','QuestionSection1','PointsEarned','PointsPossibleDisplay']
    final_headers=['sitename','reviewer', 'date','final_score','sessionid','Section','points_earned_','points_possible_','agent_name','office_depot_id']

    ################ BASIC CLEANING
    df.dropna(inplace=True)
    df=df[df['Textbox32']!='Textbox34']
    
    ### Redefining the headers and taking only desired columns
    df.columns=original_headers # Adding the Headers
    df=df[final_columns]        # Extracting only relevant columns

    ########################################## Separating Columns and Setting up The Data
    df[['TheName', 'Office_Depot_ID']] = df['PreName'].str.split(' - ', 4, expand=True)         #Splits the Name And ID
    df['SDate']=df['SDate'].str.replace('Date :','')                                            # Removes unwanted text                          # Removes unwanted text
    df['TheName']=df['TheName'].str.replace('Agent','')                                         # Removes unwanted text
    df['TheName'] = df['TheName'].str.split(',').str[::-1].str.join('')                         # Reformat the Name
    df.drop(['PreName'], axis=1, inplace=True)                                                  # Dropping unnecesary column
    df.columns=final_headers                                                                 # Changing Headers
    df['date']=df['date'].astype('datetime64[ns]')
    df['date']=df['date'].dt.date
    df['reviewer']=df['reviewer'].str.strip()
    
    ### ##################################### Extracting the dates on Database
    #lob = info_transform_function["lob"]
    df['LOB']=lob

    df['points_earned_']=df['points_earned_'].astype('int64')
    df['points_possible_']=df['points_possible_'].astype('int64')

    ########################################## TRANSFORMATING THE DATA INTO A PIVOT
    index_columns=['sitename','reviewer','date','sessionid','LOB','agent_name','office_depot_id','final_score']
    pivot=pd.pivot_table(df,index=index_columns , columns='Section', aggfunc=np.sum )
    pivot.columns = pivot.columns.map(''.join)
    pivot = pivot.reset_index()

    pivot['final_score'] = pivot['final_score'].str.rstrip('%').astype('float') / 100.0
    pivot.columns=pivot.columns.str.lower()
    
    pivot = dfutils.df_handling(pivot, info_transform_function["df_handling"])
    pivot = dfutils.fill_dataframe_nulls(pivot)

    return pivot

def agent_activity_team_time(df, info_transform_function):
    ## RELEVANT LISTS
    new_headers=['office_depot_id','agent_name','thedate','team_name','staff_hours','total_time','call_count','idle_time','idle_lunch','idle_break','acw_hours','idle_coach','idle_train','idle_meeting','idle_spec','idle_obp','idle_other','available_time','hold_count','hold_time','handle_time','wrap_time','ring_time','not_resp_time']
    final_columns=['AgentID3','AgentName2','SDate','TeamName','StaffHours','TotalTime','CallCt','IdleTime','IdleLunch','IdleBreak','IdleCall','IdleCoach','IdleTrain','IdleMeeting','IdleSpec','IdleOBP','IdleOther','AvailableTime','HoldCount','HoldTm','HandleTime','WrapTime','RingTime','NotRespTime']
    primaries_keys=['office_depot_id','agent_name','thedate','team_name']
    df['SDate']=df['SDate'].astype('datetime64[ns]')              # Converting date type
    df=df[final_columns]                                          # Taking relevant columns
    df.columns=new_headers                                        # Changing headers
    df.drop_duplicates(subset=primaries_keys, inplace=True)       # Dropping Duplicate entries
    
    number_rows=df.shape[0]
    print("Rows to be imported :", number_rows)

    df['agent_name'].fillna('' , inplace=True)                  ## for the guy who has ID but no name

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    df = dfutils.fill_dataframe_nulls(df)

    return df

def office_depot_cjp_agent_summary(df, info_transform_function):
    ############  RELEVANT LISTS
    final_columns=['Agent','Date','Calls Handled','Staff Hours','Initial Login Time','Final Logout Time','Total Available Time','Total Inbound Talk Time','Total Inbound Hold Time','Total Inbound Connected Time','Total Outdial Talk Time','Total Outdial Hold Time','Total Outdial Connected Time','Total Inbound Wrap Up Time','Total Outdial Wrap Up time',]
    new_headers=['agent_id','thedate','calls_handled','staff','initial_login_time','final_logout_time','total_available_time','total_inbound_talk_time','total_inbound_hold_time','total_inbound_connected_time','total_outdial_talk_time','total_outdial_hold_time','total_outdial_connected_time','total_inbound_wrap_up_time','total_outdial_wrap_up_time']
    time_columns=['staff','total_available_time','total_inbound_talk_time','total_inbound_hold_time','total_inbound_connected_time','total_outdial_talk_time','total_outdial_hold_time','total_outdial_connected_time','total_inbound_wrap_up_time','total_outdial_wrap_up_time']

    # ############  QUICK CLEANING
    df=df[df['Date'].notnull()]
    df=df[df['Channel']!='Voice']
    df=df[final_columns]                                           # Dropping unnecesary columns
    df.columns=new_headers                                              # Changing headers
    df['thedate']=df['thedate'].astype('datetime64[ns]')           # Changing date type
    df['thedate']=df['thedate'].astype('str')
    df['initial_login_time']=df['initial_login_time'].astype('datetime64[ns]')           # Changing date type
    df['final_logout_time']=df['final_logout_time'].astype('datetime64[ns]')           # Changing date type

    # ############  MANIPULATING THE COLUMNS WITH DURATION INFORMATION
    for i in time_columns:
        df[['Hours', 'Minutes','Seconds']] = df[i].str.split(':', 4, expand=True)
        df[['Hours', 'Minutes','Seconds']]=df[['Hours', 'Minutes','Seconds']].astype('int64')
        df.drop(columns=i, axis=1, inplace=True)
        df[i+'_sec']=df['Hours']*3600+df['Minutes']*60+df['Seconds']
        df[i+'_sec']=df[i+'_sec'].astype('int64')
        df.drop(columns=['Hours', 'Minutes','Seconds'], axis=1, inplace=True)    

    df.columns = info_transform_function["output_columns"]

    df['agent_id']=df['agent_id'].str.strip().str.upper()

    df = dfutils.df_handling(df, info_transform_function["df_handling"])    
    df = dfutils.fill_dataframe_nulls(df)

    return df

def office_depot_cjp_calls_handled_queue(df, info_transform_function):
    df['Date']=df['Date'].astype('datetime64[ns]')
    df['Date']=df['Date'].astype('str')

    sites = ['Itel - GY', 'Itel - WAH']
    df = df[df['Site'].isin(sites)]

    today=datetime.date.today()
    drop_indexes=df[df['Queue']=='Total'].index
    df.columns = info_transform_function["output_columns"]
    df.drop(drop_indexes, axis=0, inplace=True)
    df=df[df['thedate']<str(today)]


    df = dfutils.df_handling(df, info_transform_function["df_handling"])    
    df = dfutils.fill_dataframe_nulls(df)

    return df 

def office_depot_external_qa_detail(df, info_transform_function, lob):
    ### RELEVANT LISTS
    original_headers=['PreName','SiteName','Reviewer','SDate','Textbox36','SessionID','Textbox16','QuestionSection1','PointsEarned1','PointsEarned2','QuestionText','Answer','PointsEarned','PointsPossibleDisplay','Textbox2']
    final_columns=['PreName','SiteName','Reviewer', 'SDate','Textbox36','SessionID','QuestionSection1','PointsEarned','PointsPossibleDisplay']
    final_headers=['sitename','reviewer', 'date','final_score','sessionid','Section','points_earned_','points_possible_','agent_name','office_depot_id']

    ################ BASIC CLEANING
    df.dropna(inplace=True)
    df=df[df['Textbox32']!='Textbox34']
    
    ### Redefining the headers and taking only desired columns
    df.columns=original_headers # Adding the Headers
    df=df[final_columns]        # Extracting only relevant columns

    ########################################## Separating Columns and Setting up The Data
    df[['TheName', 'Office_Depot_ID']] = df['PreName'].str.split(' - ', 4, expand=True)         #Splits the Name And ID
    df['SDate']=df['SDate'].str.replace('Date :','')                                            # Removes unwanted text                          # Removes unwanted text
    df['TheName']=df['TheName'].str.replace('Agent','')                                         # Removes unwanted text
    df['TheName'] = df['TheName'].str.split(',').str[::-1].str.join('')                         # Reformat the Name
    df.drop(['PreName'], axis=1, inplace=True)                                                  # Dropping unnecesary column
    df.columns=final_headers                                                                 # Changing Headers
    df['date']=df['date'].astype('datetime64[ns]')
    df['date']=df['date'].dt.date
    df['reviewer']=df['reviewer'].str.strip()
    
    ### ##################################### Extracting the dates on Database
    #lob = info_transform_function["lob"]
    df['LOB']=lob

    df['points_earned_']=df['points_earned_'].astype('int64')
    df['points_possible_']=df['points_possible_'].astype('int64')

    ########################################## TRANSFORMATING THE DATA INTO A PIVOT
    index_columns=['sitename','reviewer','date','sessionid','LOB','agent_name','office_depot_id','final_score']
    pivot=pd.pivot_table(df,index=index_columns , columns='Section', aggfunc=np.sum )
    pivot.columns = pivot.columns.map(''.join)
    pivot = pivot.reset_index()

    pivot['final_score'] = pivot['final_score'].str.rstrip('%').astype('float') / 100.0
    pivot.columns=pivot.columns.str.lower()
    
    pivot = dfutils.df_handling(pivot, info_transform_function["df_handling"])
    pivot = dfutils.fill_dataframe_nulls(pivot)

    return pivot    

def office_depot_crm_phones(df, info_transform_function):
    # RELEVANT LISTS
    final_columns=['SDate','agent_name','Office_Depot_ID','AOPS_ID','Reference','Q1','Q2','Q3','Q4','QueueName']
    final_headers=['date','agent_name','office_depot_id','aops_id','reference','connect_text','resolve_text','ease_text','ltr','queue_name']
    primary_keys=['office_depot_id','agent_name','date','reference']
    ## SEPARATING COLUMNS
    df[['agent_name', 'Office_Depot_ID','AOPS_ID']] = df['NTLogon1'].str.split(' - ', 4, expand=True)
    df.drop(['NTLogon1'], axis=1, inplace=True)
    df=df[final_columns]
    df['SDate']=df['SDate'].astype('datetime64[ns]')

    df.replace(to_replace='' , value=np.nan, inplace=True)
    df.columns=final_headers
    df.drop_duplicates(subset=primary_keys , inplace=True)
    df.dropna( axis=0, how='any',thresh=None,  subset=['office_depot_id','agent_name','date','reference'], inplace=True,)
    number_rows=df.shape[0]
    print('Rows to be imported: ',number_rows)
    
    # One Hot Coding the CRM
    df['connect_score']=np.where(df['connect_text']=='Yes', 1, 0)
    df['resolve_score']=np.where(df['resolve_text']=='Yes', 1, 0)
    df['ease_score']=np.where(df['ease_text']=='Yes', 1, 0)
    # Calculating the NPS Variables
    df["promoters"]=np.where(df['ltr']>8, 1, 0)
    df["detractors"]=np.where(df['ltr']<=6, 1, 0)
    df["passives"]=np.where(df['ltr'].isin([7,8]), 1, 0)
       
    df.columns=df.columns.str.lower()

    df["office_depot_id"] = df["office_depot_id"].astype('str')
    df["office_depot_id"] = df["office_depot_id"].apply(lambda txt: txt.split(".")[0])    

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    df = dfutils.fill_dataframe_nulls(df)    

    return df

def office_depot_crm_sms(df, info_transform_function):
    # RELEVANT LISTS
    final_columns=['SDate','agent_name','Office_Depot_ID','AOPS_ID','Reference','Q1','Q2','Q3','Q4','QueueName']
    final_headers=['date','agent_name','office_depot_id','aops_id','reference','connect_text','resolve_text','ease_text','ltr','queue_name']
    primary_keys=['office_depot_id','agent_name','date','reference']
    ## SEPARATING COLUMNS
    print("Separating columns in function.")
    df['AOPS_ID']=''
    df[['agent_name', 'Office_Depot_ID']] = df['NTLogon1'].str.split(' - ', 4, expand=True)
    df.drop(['NTLogon1'], axis=1, inplace=True)
    df=df[final_columns]
    df['SDate']=df['SDate'].astype('datetime64[ns]')

    df.replace(to_replace='' , value=np.nan, inplace=True)
    print("Rename in function.")
    df.columns=final_headers
    df.drop_duplicates(subset=primary_keys , inplace=True)
    df.dropna( axis=0, how='any',thresh=None,  subset=['office_depot_id','agent_name','date','reference'], inplace=True,)
    number_rows=df.shape[0]
    print('Rows to be imported: ',number_rows)
    
    # One Hot Coding the CRM
    df['connect_score']=np.where(df['connect_text']=='Yes', 1, 0)
    df['resolve_score']=np.where(df['resolve_text']=='Yes', 1, 0)
    df['ease_score']=np.where(df['ease_text']=='Yes', 1, 0)
    # Calculating the NPS Variables
    df["promoters"]=np.where(df['ltr']>8, 1, 0)
    df["detractors"]=np.where(df['ltr']<=6, 1, 0)
    df["passives"]=np.where(df['ltr'].isin([7,8]), 1, 0)
    
    df.columns=df.columns.str.lower()

    df["office_depot_id"] = df["office_depot_id"].astype('str')
    df["office_depot_id"] = df["office_depot_id"].apply(lambda txt: txt.split(".")[0])      

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    df = dfutils.fill_dataframe_nulls(df)    

    return df


def office_depot_crm_chat(df, info_transform_function):
    # RELEVANT LISTS
    final_columns=['SDate','agent_name','Office_Depot_ID','AOPS_ID','Reference','Q1','Q2','Q3','Q4','QueueName']
    final_headers=['date','agent_name','office_depot_id','aops_id','reference','connect_text','resolve_text','ease_text','ltr','queue_name']
    primary_keys=['office_depot_id','agent_name','date','reference']
    ## SEPARATING COLUMNS
    df['QueueName']='Chat'
    df[['agent_name', 'Office_Depot_ID','AOPS_ID']] = df['NTLogon1'].str.split(' - ', 4, expand=True)
    df.drop(['NTLogon1'], axis=1, inplace=True)
    df=df[final_columns]
    df['SDate']=df['SDate'].astype('datetime64[ns]')
    
    df.replace(to_replace='' , value=np.nan, inplace=True)
    df.columns=final_headers
    df.drop_duplicates(subset=primary_keys , inplace=True)
    df.dropna( axis=0, how='any',thresh=None,  subset=['office_depot_id','agent_name','date','reference'], inplace=True,)
    number_rows=df.shape[0]
    print('Rows to be imported: ',number_rows)
    
    # One Hot Coding the CRM
    df['connect_score']=np.where(df['connect_text']=='Yes', 1, 0)
    df['resolve_score']=np.where(df['resolve_text']=='Yes', 1, 0)
    df['ease_score']=np.where(df['ease_text']=='Yes', 1, 0)
    # Calculating the NPS Variables
    df["promoters"]=np.where(df['ltr']>8, 1, 0)
    df["detractors"]=np.where(df['ltr']<=6, 1, 0)
    df["passives"]=np.where(df['ltr'].isin([7,8]), 1, 0)
    
    df.columns=df.columns.str.lower()

    df["office_depot_id"] = df["office_depot_id"].astype('str')
    df["office_depot_id"] = df["office_depot_id"].apply(lambda txt: txt.split(".")[0])      

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    df = dfutils.fill_dataframe_nulls(df)    

    return df