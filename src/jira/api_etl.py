import pandas as pd
import utils.utils as utils
import utils.dfutils as dfutils
import utils.dbutils as dbutils
from src.jira.configs import configs
from src.jira.jira_utils import construct_map_table, normalize_values, dsi_users, get_needed_data_by_query

def jira_api_etl(casename):
    print(f"Working on {casename} case!")
    ignored_keys = ["decryption_key", "user", "jira_domain"]
    credentials_name = "atlassian_jira_api"
    credentials = utils.get_decrypted_credential(ignored_keys, credentials_name)
    user = credentials["user"]
    token = credentials["token"]
    jira_domain = credentials["jira_domain"]
    case_config = configs[casename]
    query_data = case_config["query_data"]
    schema = case_config["schema"]
    table_name = case_config["table_name"]
    if query_data:
        conn = dbutils.open_connection_with_scripting_account()
        jira_needed_data = get_needed_data_by_query(conn, query_data)
    else:
        get_all_data_function = case_config["get_all_data_function"]
        jira_needed_data = get_all_data_function(user, token, jira_domain)
    
    
    get_data_with_details_function = case_config["get_data_with_details_function"]
    
    if casename == "projects":
        jira_detailed_data = pd.DataFrame(get_data_with_details_function(jira_needed_data))
    elif casename == "users":
        jira_detailed_data = pd.DataFrame(get_data_with_details_function(jira_needed_data, dsi_users))
    else:
        jira_detailed_data = pd.DataFrame(get_data_with_details_function(jira_domain, user, token, jira_needed_data))
        
    columns_to_normalize = case_config["columns_to_normalize"]
    if columns_to_normalize:
        all_aux_tables = []
        for column in columns_to_normalize:
            aux_table, dicc_to_replace = construct_map_table(jira_detailed_data, column)
            all_aux_tables.append(pd.DataFrame(aux_table))
            jira_detailed_data = normalize_values(jira_detailed_data, column, dicc_to_replace)
        
        aux_tables_names = case_config["aux_tables_names"]
        for i in range(len(aux_tables_names)):
            aux_table_to_upload = pd.DataFrame(all_aux_tables[i])
            aux_table_to_upload = dfutils.fill_dataframe_nulls(aux_table_to_upload)
            aux_table_name = aux_tables_names[i]
            try:
                print(aux_table_to_upload)
                conn = dbutils.open_connection_with_scripting_account()
                dbutils.perform_safe_truncate_insert(aux_table_to_upload, conn, schema, aux_table_name)
            except Exception as e:
                print(f"Oops! Something went wrong: {e}")

        date_columns = case_config["date_columns"]
        if date_columns:
            for column in date_columns:
                jira_detailed_data[column] = pd.to_datetime(jira_detailed_data[column])
            jira_detailed_data = dfutils.validate_datetime_columns(jira_detailed_data, date_columns, date_format="%Y-%m-%d %H:%M:%S.%f%z")
            
        foreign_to_rename = case_config["foreign_to_rename"]
        jira_detailed_data = jira_detailed_data.rename(columns=foreign_to_rename)
        
    
    try:
        df_to_upload = dfutils.fill_dataframe_nulls(jira_detailed_data)
        print(df_to_upload)
        conn = dbutils.open_connection_with_scripting_account()
        dbutils.perform_safe_truncate_insert(df_to_upload, conn, schema, table_name)
    except Exception as e:
        print(f"Oops! Something went wrong: {e}")
            



def main(optional: list):
    """ Runs the extract_transform_and_load_data function.
    Args:
        optional (int): Run mode.
    """

    match optional[0]:
        case 1:
            jira_api_etl("projects")
        case 2:
            jira_api_etl("users")
        case 3:
            jira_api_etl("boards")
        case 4:
            jira_api_etl("sprints")
        case 5:
            jira_api_etl("issues_sprint")