# Python modules
import argparse
import importlib
from datetime import datetime as dt
import utils.utils as utils
import utils.dbutils as dbutils
import utils.dfutils as dfutils
import getpass 
import pandas as pd

def etl_script_execution_log(script_name, script_id, optional_parameters, end_time):
        try:
            print('Opening database connection.') # Open Connection with database
            conn = dbutils.open_connection_with_scripting_account() # Perform a connection to the database
            cursor = conn.cursor()                                                                           
            cursor.fast_executemany = True

            if isinstance(optional_parameters, list): secondary_script_id = optional_parameters[0] 
            else: secondary_script_id = None

            ran_by = getpass.getuser()  # Gets user of machine running code
            data = [[script_id, script_name, secondary_script_id, ran_by, end_time]]
            columns = ["script_id", "script_name", "optional_parameter", "ran_by", "ran_on"]
            schema = "misc"
            table_name = "etl_script_execution"

            df = pd.DataFrame(data = data, columns = columns)

            df = dfutils.fill_dataframe_nulls(df)
            
            dbutils.perform_insert(conn, df, schema, table_name)            

            print("-------RUN LOG UPDATED-------------")
        except Exception as e:
            conn.rollback()
            print('Script execution log entry not updated, rolling back to previous state \n Error Details: ', e)        

if __name__ == '__main__':
    # Gets the configuration file JSON as a dictionary from the config package.
    runner_config = utils.get_config('runner_config_file')

    # Parse the arguments. Creaate the argument parser, define the argument and read the argument.
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--id", required=True, help="The ID of the script to be run.", type=int)
    ap.add_argument("-o", "--optional", nargs='*', required=False, help="Optional parameters to be passed to the main function.", type=int)
    script_id = str(vars(ap.parse_args())['id'])
    optional_parameters = vars(ap.parse_args())['optional']

    # Verify if the key exists, print error if not, execute if yes    
    if script_id in runner_config:
#        try: 
        # Run if exists
        start_time = dt.now()
        script_path = runner_config[script_id]["script_path"]
        script_name = runner_config[script_id]["script_name"]
        script_description = runner_config[script_id]["script_description"]
        mymodule = importlib.import_module(script_path)

        # Logging messages
        print("-----------RUNNING SCRIPT-----------")
        print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Script path: {script_path}")
        print(f"Script name: {script_name}")
        print(f"Script ID: {script_id}")
        print(f"Script parameters: {optional_parameters}")
        print(f"Script description: {script_description }")
        print("------------------------------------")

        # Run the script 
        mymodule.main(optional_parameters)

        # More logging messages
        print("------------------------------------")
        end_time = dt.now()
        print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {(end_time-start_time).total_seconds()} seconds")
        print("----------SCRIPT COMPLETED----------")

        # Update the run log
        print("-------UPDATING SCRIPT RUN LOG------")
        etl_script_execution_log(script_name, script_id, optional_parameters, end_time)

#        except Exception as e:
#            # Raise exception otherwise
#            raise Exception(e)
    else: 
        # If script ID is not found raise value error
        raise ValueError(f"The script ID provided: {script_id} does not exist.")
