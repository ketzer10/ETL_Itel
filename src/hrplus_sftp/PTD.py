import pyodbc
import pandas as pd
import numpy as np

from datetime import date, timedelta

import utils.dbutils as dbutils

##Get Date
today = date.today()

if today.weekday() == 0:
    
    time_delta = timedelta(2)
else:
    time_delta = timedelta(1)

desire_date = str(today-time_delta)
FINAL_DATE = desire_date.replace('-','')

##If weekend
FINAL_DATE_2 = (str(today-timedelta(1))).replace('-','')

QUERY_ALTICE = f"SELECT A.date, A.not_ready_reason_code, sum(A.not_ready_reason_duration) AS duration, A.ps_id FROM altice.glb_optimum_nrrc AS A \
WHERE A.date >= '{FINAL_DATE}' GROUP BY A.date, A.not_ready_reason_code, A.ps_id \
UNION ALL \
SELECT A.date, A.not_ready_reason_code, sum(A.not_ready_reason_duration) AS duration, A.ps_id FROM altice.glb_mobile_nrrc AS A \
WHERE A.date >= '{FINAL_DATE}' GROUP BY A.date, A.not_ready_reason_code, A.ps_id \
UNION ALL \
SELECT A.date, A.not_ready_reason_code, sum(A.not_ready_reason_duration) AS duration, A.ps_id FROM altice.glb_suddenlink_nrrc AS A \
WHERE A.date >= '{FINAL_DATE}' GROUP BY A.date, A.not_ready_reason_code, A.ps_id"

QUERY_MASTER_ALTICE = f"SELECT * FROM altice.glb_alignments"

QUERY_TDS = f"WITH tmp_no_break AS( SELECT B.hrm_id, \
       A.reason_desc, \
       CONVERT(DATE, A.status_start) AS status_start, \
       SUM(status_duration_sec) AS duration \
FROM tds.glb_agent_status AS A \
LEFT JOIN tds.hrm_employee_id AS B ON A.aspect_id = B.tds_id \
WHERE A.date >= '{FINAL_DATE}' AND hrm_id IS NOT NULL AND A.reason_desc IS NOT NULL AND A.reason_desc <> 'Break' \
GROUP BY B.hrm_id, CONVERT(DATE, A.status_start), A.reason_desc), \
tmp_break AS( \
SELECT B.hrm_id, \
       A.reason_desc, \
       A.status_start, \
       status_duration_sec AS duration \
FROM tds.glb_agent_status AS A \
LEFT JOIN tds.hrm_employee_id AS B ON A.aspect_id = B.tds_id \
WHERE A.date >= '{FINAL_DATE}' AND hrm_id IS NOT NULL AND A.reason_desc IS NOT NULL AND A.reason_desc = 'Break'), \
tmp_joined AS( \
    SELECT hrm_id, reason_desc, status_start, duration \
    FROM tmp_no_break \
    UNION ALL \
    SELECT hrm_id, reason_desc, status_start, duration \
    FROM tmp_break) \
SELECT hrm_id, reason_desc AS aux_code_name, duration, CONVERT(DATE, A.status_start) AS date \
FROM tmp_joined AS A \
ORDER BY A.hrm_id, A.status_start, A.reason_desc"

RENAME_COLUMNS = {
                    'HRMID': 'hrm_id',
                    'not_ready_reason_code': 'aux_code_name'
                    }

def main (optional: list):

    print(optional)

    cnxn = dbutils.open_connection_with_scripting_account()

    match optional[0]:

        case 1:
            ##PTD_TDS
            print('TDS PTD report')
            print('Getting data')
            df_tds = get_data_server(QUERY_TDS, cnxn)
            df_tds[['duration']] = df_tds[['duration']].astype('Int64')

            print(df_tds)

            if today.weekday() == 1:
                df_tds.to_csv(f'./src/tds/data/PTD_TDS_{FINAL_DATE}_{FINAL_DATE}.csv', sep=',', index=False)
            else:
                df_tds.to_csv(f'./src/tds/data/PTD_TDS_{FINAL_DATE}_{FINAL_DATE_2}.csv', sep=',', index=False)
        
        case 2:
           ###PTD_ALTICE
            print('Altice PTD report')
            df_sql = get_data_server(QUERY_ALTICE, cnxn)
            df_master = get_data_server(QUERY_MASTER_ALTICE, cnxn)
            df = merge_dfs(df_sql, 'ps_id', df_master, 'ps_id')
            df = delete_columns(df, ['report_agent_name', 'ps_id'])
            df = rename_columns(df, RENAME_COLUMNS)
            df = remove_nan_column(df)
            df = df[['hrm_id', 'aux_code_name', 'duration', 'date']]
            df['hrm_id'] = df['hrm_id'].astype(int)
            df['duration'] = df['duration'].astype(int)
        
            print(df)
            
            
            if today.weekday() == 1:
                df.to_csv(f'./src/altice/data/PTD_Altice_{FINAL_DATE}_{FINAL_DATE}.csv', sep=',', index=False)
            else:
                df.to_csv(f'./src/altice/data/PTD_Altice_{FINAL_DATE}_{FINAL_DATE_2}.csv', sep=',', index=False)
 
 
    ##CLOSE SQL CONNECTION
    close_connection = close_bd_connection(cnxn)


def get_data_server(query, connection):
    
    df = pd.read_sql(query, connection)

    return df

def read_file(path):

    df = pd.read_csv(path, sep=';')

    return df

def merge_dfs(df1, df1column, df2, df2column):

    df = df1.merge(df2, left_on=df1column, right_on=df2column)

    return df

def delete_columns(df, columns):

    df = df.drop(columns, axis=1)

    return df

def rename_columns(df, names_dict):

    df.rename(columns = names_dict, inplace = True)

    return df

def remove_nan_column(df):

    df = df.dropna()

    return df

def close_bd_connection(connection):

    csr = connection.cursor()
    csr.close()
    del csr

    return 'Connection closed'

