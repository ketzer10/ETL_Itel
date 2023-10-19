# import packages
from datetime import date
import datetime
import utils.dfutils as dfutils
import pandas as pd
import numpy as np

def transform_function_agent_snapshot(df: pd.DataFrame, info_transform_function: dict, **kwargs) -> pd.DataFrame:

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    df = df.dropna(subset = ["date", "agent_name"])
    df["occupancy"] = df["occupancy"]/100

    return df

def transform_function_agent_time_card(df: pd.DataFrame, info_transform_function: dict, **kwargs) -> pd.DataFrame:

    df.drop(df[df['Agent Session'] == "Total"].index, inplace = True)
    df.drop(df[df['Agent Name (ID)'] == "Total"].index, inplace = True)

    lista = []
    def agent(value):
        if len(str(value)) > 4:
            lista.append(str(value).strip())
            return str(value).strip()
        else:
            return lista[-1]

    def duration(string):
        components = string.split(":")
        if len(components) == 3:
            return int(components[0])*3600 + int(components[1])*60 + int(components[2])
        elif len(components) == 2:
            return int(components[0])*60 + int(components[1])

    #adding date column from the file name
    df["Date"] = kwargs["file_name"].split(" ")[0]
    
    df["Team Name (ID)"] = df["Team Name (ID)"].apply(agent)
    df['team_name_id'] = df["Team Name (ID)"].str.extract(r'(\([^)]*\))', expand=True)
    df["team_name_id"] = df["team_name_id"].astype('str')
    df['team_name_id'] = df['team_name_id'].str.replace('(','', regex=True)
    df['team_name_id'] = df['team_name_id'].str.replace(')','', regex=True)
    
    df["Agent Name (ID)"] = df["Agent Name (ID)"].apply(agent)
    df['agent_id'] = df["Agent Name (ID)"].str.extract(r'(\([^)]*\))', expand=True)
    df["agent_id"] = df["agent_id"].astype('str')
    df['agent_id'] = df['agent_id'].str.replace('(','', regex=True)
    df['agent_id'] = df['agent_id'].str.replace(')','', regex=True)

    df.dropna(inplace=True)
    
    df["Team Name (ID)"] = df["Team Name (ID)"].replace('\([^)]*\)', '', regex=True)  
    df["Agent Name (ID)"] = df["Agent Name (ID)"].replace('\([^)]*\)', '', regex=True)  

    df["duration_sec"] = df["Duration"].apply(duration)

    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    # df["date"] = df["login_date"].dt.date   
    # df["date"] = df["date"].astype('datetime64[ns]')

    return df

def transform_function_coaching_fs_meeting(df: pd.DataFrame, info_transform_function: dict, **kwargs) -> pd.DataFrame:

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    df = df[df["date"] >= datetime.datetime(2022, 3, 1)]

    return df

def transform_function_sys_issues(df: pd.DataFrame, info_transform_function: dict, **kwargs) -> pd.DataFrame:

    df = dfutils.df_handling(df, info_transform_function["df_handling"])
    df = df[df["date"] >=  datetime.datetime(2022, 4, 1)] 

    return df

def transform_function_unavailable_time(df: pd.DataFrame, info_transform_function: dict, **kwargs) -> pd.DataFrame:

    lista = []
    def agent(value):
        
        if len(str(value)) > 4:
            lista.append(str(value).strip())
            return np.nan
        else:
            return lista[-1]
    
    #adding date column from the file name
    df["Date"] = kwargs["file_name"].split(" ")[0]
    # Filling rows empty
    df["Agent Name (ID)"] = df["Agent Name (ID)"].apply(agent)
    # dropt na rows
    df.dropna(inplace=True)
    # separating id and agent_name
    df['id'] = df["Agent Name (ID)"].str.extract(r'(\([^)]*\))', expand=True)
    df["id"] = df["id"].astype('str')
    df['id'] = df['id'].str.replace('(','', regex=True)
    df['id'] = df['id'].str.replace(')','', regex=True)
    df["Agent Name (ID)"] = df["Agent Name (ID)"].replace('\([^)]*\)','',regex=True)
    # apply df_utils
    df = dfutils.df_handling(df, info_transform_function["df_handling"])

    return df