# import packages
import utils.dfutils as dfutils
import pandas as pd
import numpy as np

def transforms_csat_results(df: pd.DataFrame, info_transform_function: dict) -> pd.DataFrame:
    
    df.columns=['id','description','value']
    df=df[['value']]
    df['value']=df['value'].astype('str')
    df=df[df['value'].str.contains('CSV')]
    df[['date','dnis','ani','full_name','sklname','question1','question2','question3']]=df['value'].str.split("|",expand=True)
    df=df[['date','dnis','ani','full_name','sklname','question1','question2','question3']]
    df['date']=df['date'].str.replace('CSV::','')
    df['date']=df['date'].str.replace('";"',' ')
    df = dfutils.df_handling(df, info_transform_function["df_handling"])
          
    return df

