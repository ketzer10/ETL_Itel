# import packages
import utils.dfutils as dfutils
import pandas as pd
import numpy as np

def transforms_function_glb_cx_daily_scores(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    raw_data = df.get('Raw Data 2023')
 
    cols_to_drop = raw_data.filter(like='MTD').columns
    raw_data = raw_data.drop(columns=cols_to_drop)

    raw_data = pd.melt(raw_data, id_vars=["Location","SVP","Manager","Business Unit","Metrics"], var_name="Date")

    historic = ["Raw Data 2022","January 2021","February 2021","March 2021","April 2021","May 2021","June 2021 ","July 2021","August 2021","September 2021","October 2021","November 2021","December 2021"]
    for dataframe in historic:
        
        temp = df.get(dataframe)
        
        temp = temp.rename(columns={ 
            temp.columns[0]: "Location",
            temp.columns[1]: "SVP",
            temp.columns[2]: "Manager",
            temp.columns[3]: "Business Unit",
            temp.columns[4]: "Metrics"
        })

        # Delete Columns
        if dataframe == "July 2021":
            temp.columns = [str(i).replace('-','/').replace(' 00:00:00','') for i in temp.columns.to_list()]

        columns = temp.columns.to_list()
        delete = [i for i in columns if "/" not in str(i) and str(i) not in ["Location","SVP","Manager","Business Unit","Metrics"]]
        temp = temp.drop(delete, axis=1)

        temp = pd.melt(temp, id_vars=["Location","SVP","Manager","Business Unit","Metrics"], var_name="Date")

        raw_data = raw_data.append(temp)
    
    raw_data['Date'] = pd.to_datetime(raw_data['Date'], errors = 'coerce')

    df = dfutils.df_handling(raw_data, info_transform_function["df_handling"])

    return df

def transforms_function_glb_cx_daily_scores_mtd(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame: 

    raw_data = df.get('Raw Data 2023')



    cols_to_drop = raw_data.filter(like=':').columns
    cols_to_drop = cols_to_drop.append(raw_data.filter(like='/').columns)
    raw_data = raw_data.drop(columns=cols_to_drop)

    raw_data.columns = raw_data.columns.str.replace('MTD ', '')
    raw_data = pd.melt(raw_data, id_vars=["Location","SVP","Manager","Business Unit","Metrics"], value_name="MTD")
    raw_data[['Month','Year']] = raw_data.variable.str.split(" ",expand=True)

    del raw_data["variable"]

    historic = ["Raw Data 2022","January 2021","February 2021","March 2021","April 2021","May 2021","June 2021 ","July 2021","August 2021","September 2021","October 2021","November 2021","December 2021"]
    for dataframe in historic:
    
        temp = df.get(dataframe)
        temp = temp.rename(columns={ 
            temp.columns[0]: "Location",
            temp.columns[1]: "SVP",
            temp.columns[2]: "Manager",
            temp.columns[3]: "Business Unit",
            temp.columns[4]: "Metrics"
        })

        columns = temp.columns.to_list()
        delete = [i for i in columns if "MTD" not in str(i) and str(i) not in ["Location","SVP","Manager","Business Unit","Metrics"]]
        temp = temp.drop(delete, axis=1)
    
        temp.columns = temp.columns.str.replace('MTD ', '')

        temp = pd.melt(temp, id_vars=["Location","SVP","Manager","Business Unit","Metrics"], value_name="MTD")
     
        temp[['Month','Year']] = temp.variable.str.split(" ",expand=True)
        del temp["variable"]

        raw_data = raw_data.append(temp)

    raw_data = dfutils.df_handling(raw_data, info_transform_function["df_handling"])

    return raw_data