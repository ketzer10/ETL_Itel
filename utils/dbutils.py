from os import replace
import pyodbc
import pandas as pd
import numpy as np
import itertools
import utils.utils as utils

def open_connection(hostname: str, database: str, username: str, password: str, autocommit: bool = False) -> pyodbc.Connection:
    """Returns a pyodbc connection object using the parameters provided

    Args:
        hostname (str): The hostname or IP address of the database.
        database (str): The database to which the connection will be made.
        username (str): The SQL Server username.
        password (str): The SQL Server password.

    Returns:
        pyodbc.Connection: A connection object to the database.
    """
    connstring = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={hostname};DATABASE={database};UID={username};PWD={password}"
    conn = pyodbc.connect(connstring, autocommit = autocommit)

    return conn

def open_connection_with_scripting_account() -> pyodbc.Connection:
    """Returns a pyodbc connection object with the connection performed to the Azure itel_datasi database using the 
    scripting account. A convenience method to automatically connect to this specific database with this specific user.

    Returns:
        [pyodbc.Connection]: A connection object to the itel_datasi database with the scripting user and password.
    """

    # Get the database configurations
    database_configs = utils.get_config('database_configs')
    database_name = database_configs['azure_sql_server_itel_datasi']['database_name']

    # Get the username and password for the scripting account
    db_credentials = utils.get_decrypted_credential(['decryption_key'], 'sql_server_scripting_user')

    conn = open_connection(database_configs['azure_sql_server_itel_datasi']['hostname'], 
                           database_configs['azure_sql_server_itel_datasi']['database_name'], 
                           db_credentials['username'], db_credentials['password'])

    return conn

def open_postgresql_connection(hostname: str, database: str, username: str, password: str, autocommit: bool = False) -> pyodbc.Connection:
    """Returns a pyodbc connection object using the parameters provided

    Args:
        hostname (str): The hostname or IP address of the database.
        database (str): The database to which the connection will be made.
        username (str): The SQL Server username.
        password (str): The SQL Server password.

    Returns:
        pyodbc.Connection: A connection object to the database.
    """
    connstring = f"DRIVER={{PostgreSQL Unicode}};SERVER={hostname};DATABASE={database};UID={username};PWD={password}"
    conn = pyodbc.connect(connstring, autocommit = autocommit)

    return conn


def generate_dataframe_upsert_stmt(keys: list, source_df: pd.DataFrame, target_table_name: str) -> dict:
    """Generate the SQL statement and parameters required to perform a SQL 'upsert', also known as a merge.
    The dataframe has to have the same columns as the target table. The keys list should be a subset of the 
    dataframe columns. If it is not, an error will occurr when tryin to run the statement.

    Args:
        keys (list): A list containing the column names to be used as keys for the merge statement.
        source_df (pd.DataFrame): The DataFrame that will be inserted into the database.
        target_table_name (str): The name and schema of the target table. Eg. schema.table_name

    Returns:
        stmt_data (dict): A dictionary containing the statement data. The key "stmt" contains the parametrized query 
        to be ran in the database. The "params" key contains the data to be passed to the statement.
    """

    # Convert the dataframe columns to a list and join them into  string tuple: Eg. '(name, date, metric)'
    cols_list = source_df.columns.tolist()
    cols_list_query = f'({(", ".join(cols_list))})'

    # Check if keys list is subset of column list
    if not (set(keys).issubset(cols_list)):
        raise ValueError('List of keys is not a subset of DataFrame column list. Cannot perform UPSERT operation.')


    # Create the parameter slots. This is the question mark tuple (?, ?, ?). It depends on the number of
    # columns in the dataframe
    param_slots = '('+', '.join(['?']*len(source_df.columns))+')'

    # Create the statement for the INSERT condition. If INSERT, the values should be source.col1,
    # source.col2, etc since those were already defined. We could also pass the values themselves 
    # as a parameter. 
    sr_cols_list = [f'source.{i}' for i in cols_list]
    sr_cols_list_query = f'({(", ".join(sr_cols_list))})'

    # The UPDATE operation only requires us to update the values which are NOT keys. 
    # Then we just need to set the target columns to the source rows
    non_keys = list(set(cols_list) - set(keys))
    up_cols_list = [f'target.{i}=source.{i}' for i in non_keys]
    up_cols_list_query = f'{", ".join(up_cols_list)}'

    # Create the conditional statement on which keys will be used to check the merge conditions
    # The statement created looks like source.key1 = target.key2 AND source.key2 = target.key2 ...
    # if there is only one key the condition is source.key = target.key
    condition_stmt = None
    for index, key in enumerate(keys):
        if index == 0:
            condition_stmt = 'source.' + key + ' = ' + 'target.' + key
        else: 
            condition_stmt = condition_stmt + ' AND ' + 'source.' + key + ' = ' + 'target.' + key

    # create the list of parameter indicators (?, ?, ?, etc...)
    # and the parameters, which are the values to be inserted
    params = source_df.values.tolist()
        
    cmd = f'''
        MERGE INTO {target_table_name} as target
        USING (SELECT * FROM
        (VALUES {param_slots})
        AS s {cols_list_query}) AS source
        ON {condition_stmt}
        WHEN NOT MATCHED THEN
        INSERT {cols_list_query} VALUES {sr_cols_list_query}
        WHEN MATCHED THEN
        UPDATE SET {up_cols_list_query};
        '''
    # Return a dictionary with the parameter values and the stmt to execute
    stmt_data = {
        "stmt": cmd,
        "params": params
    }

    return stmt_data

def generate_delete_with_key_stmt(keys: list, source_df: pd.DataFrame, schema: str, target_table_name: str) -> dict:
    """Generates a SQL delete statement and accompanying parameters that deletes from a table given a key list
    and a DataFrame. Deletes from the table if the values exist in the DataFrame columns defined by the key list.
    The statement generated is of the form: 
    DELETE FROM schema.target_table_name WHERE key1 IN (unique_value1, unique_value2...) AND key2 IN (...)
    The DataFrame columns should be the same as the target table columns.
    
    Args:
        keys (list): A list containing the name of the columns to be used as keys in the DELETE statement. 
        source_df (pd.DataFrame): The DataFrame to be compared against the target table.
        schema (str): The name of the schema in the database.
        target_table_name (str): The name of the table to be compared against.

    Raises:
        ValueError: When keys list is of length 0.
        ValueError: When keys list is not a subset of the DataFrame column names.

    Returns:
        stmt_data (dict): A dictionary containing the statement data. The key "stmt" contains the parametrized query 
        to be ran in the database. The "params" key contains the data to be passed to the statement.
    """
    
    if (len(keys) == 0):
        raise ValueError('Keys list should have at least one element. For DELETE statements without args use TRUNCATE.')
    
    # List of DataFrame columns
    cols_list = source_df.columns.tolist()

    if (not set(keys).issubset(cols_list)):
        raise ValueError('Keys list should be a subset of DataFrame columns list. Cannot perform DELETE operation.')

    # Get unique list of items the DataFrame for the keys column
    unique_list = []
    
    for key in keys:
        value_array = np.array(source_df[key].tolist())
        unique_array = np.unique(value_array).tolist()
        unique_list.append(unique_array)

    # Merge the list of lists into one
    merged_unique_list = [list(itertools.chain.from_iterable(unique_list))]

    param_holder = []
    for element in unique_list:
        if len(element) == 0:
            print("DELETE operation not performed because the provided DataFrame was empty on any of they key columns.")
            return
        else:
            param_slots = '('+', '.join(['?']*len(element))+')'
            param_holder.append(param_slots)


    condition_stmt = None
    for index, key in enumerate(keys):
        if index == 0:
            condition_stmt = key + ' IN ' + param_holder[index]
        else: 
            condition_stmt = condition_stmt + ' AND ' + key + ' IN ' + param_holder[index]    

    cmd = f'DELETE FROM {schema}.{target_table_name} WHERE {condition_stmt}'
    
    stmt_data = {
        'stmt': cmd,
        'params' : merged_unique_list
    }

    return stmt_data

def perform_safe_truncate_insert(source_df: pd.DataFrame, conn: pyodbc.Connection, schema: str, target_table_name:str)-> int:
    """Perform a safe truncate and insert protocol.
    This means the targuet table will get truncated before importing new data, however,
    if there are errors in the data the new data will not be imported and a rollback to the
    previous state of the table will be performed.

    Args:
        source_df (pd.DataFrame): The DataFrame that will be inserted into the database.
        con (pyodbc.Connection): Pyodbc Connection object.
        schema (str): The schema where the target table is.
        target_table_name (str): The name and schema of the target table. Eg. schema.table_name.
        
    Returns:
        status (int): Generic status to display if the table got updated with new data or not.
    """

    #Defining return status
    status = None
    # Opening a cursos from the connection passed as argument.
    cursor = conn.cursor()

    try:    
        # Executing truncate statement 
        cursor.execute(f'TRUNCATE TABLE {schema}.{target_table_name}')
        print(f'Table {target_table_name} was truncated')
        
        # Preparing the insert statement
        insert_stmt = generate_insert_stmt(source_df, schema, target_table_name)
        cursor.fast_executemany = True
        
        # Adding the dataframe values to the insert statement
        cursor.executemany(insert_stmt['stmt'], insert_stmt['params'])
        
        # Commiting the new values
        conn.commit()
        print(f'{len(source_df)} rows inserted to the {target_table_name} table')
        status = 1

    except Exception as e:
        # Rolling back to previous table state in case the insertion fails
        conn.rollback()
        print('Table not uploaded, rolling back to previous state \n Error Details: ', e)
        status = 0

    conn.close()
    print('Connection Closed')
    return status

def generate_insert_stmt(source_df: pd.DataFrame, schema: str, target_table_name: str) -> dict:
    """Generates an insert statement to a given schema.database given a dataframe. Dataframe columns have to match with database
    columns.

    Args:
        source_df (pd.DataFrame): The dataframe to upload to the database.
        schema (str): The schema of the database.
        target_table_name (str): The table the dataframe will be uploaded to.

    Returns:
        dict: A dictionary containing the statement data. The key "stmt" contains the parametrized query 
        to be ran in the database. The "params" key contains the data to be passed to the statement.
    """


    param_slots = '('+', '.join(['?']*len(source_df.columns))+')'
    insert_statement = f"INSERT INTO {schema}.{target_table_name} ({','.join(source_df.columns)}) VALUES {param_slots}"
    params = source_df.values.tolist()

    stmt_data = {
        "stmt": insert_statement,
        "params": params
    }

    return stmt_data

def perform_safe_delete_insert_with_keys(conn: pyodbc.Connection, delete_keys: list, source_df: pd.DataFrame, schema: str, 
                                         target_table_name: str):

    try: 
        cursor = conn.cursor()
        cursor.fast_executemany = True
        delete_stmt = generate_delete_with_key_stmt(delete_keys, source_df, schema, target_table_name)
        insert_stmt = generate_insert_stmt(source_df, schema, target_table_name)
            
        print("Deleting data from database.")
        cursor.executemany(delete_stmt['stmt'], delete_stmt['params'])
        print("Inserting data into database.")
        cursor.executemany(insert_stmt['stmt'], insert_stmt['params'])
        print("Commiting changes.")
        conn.commit()
        print(f'{len(source_df)} rows inserted to the {target_table_name} table')
        status = 1

    except Exception as e:
        # Rolling back to previous table state in case the insertion fails
        conn.rollback()
        print('Table not uploaded, rolling back to previous state \n Error Details: ', e)
        status = 0

    conn.close()
    print('Connection Closed')
    return status


def perform_insert(conn: pyodbc.Connection, source_df: pd.DataFrame, schema: str, 
                                         target_table_name: str):

    try: 
        cursor = conn.cursor()
        cursor.fast_executemany = True
        insert_stmt = generate_insert_stmt(source_df, schema, target_table_name)

        print("Inserting data into database.")
        cursor.executemany(insert_stmt['stmt'], insert_stmt['params'])
        print("Commiting changes.")
        conn.commit()
        print(f'{len(source_df)} rows inserted to the {target_table_name} table')
        status = 1

    except Exception as e:
        # Rolling back to previous table state in case the insertion fails
        conn.rollback()
        print('Table not uploaded, rolling back to previous state \n Error Details: ', e)
        status = 0

    conn.close()
    print('Connection Closed')
    return status