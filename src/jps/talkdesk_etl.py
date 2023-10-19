from src.jps.talkdesk_api_and_db_functions import *
from src.jps.talkdesk_configs import talkdesk_configs as configs
from src.jps.talkdesk_reports_configs import reports_configs

def extract_transform_and_load_data(report_name, info):
    print(f"Working on {report_name} report")
    credential_name = configs["credential_name"]
    ignored_keys = configs["ignored_keys"]
    account_name = configs["account_name"]
    report_config = reports_configs[report_name][info]
    schema = report_config["schema"]
    table_name = report_config["table_name"]
    insert_mode = report_config["insert_mode"]
    credentials = utils.get_decrypted_credential(ignored_keys, credential_name)
    all_data = []
    dates_list, conn = check_max_date_and_generate_dates_list_and_conn(table_name)
    try:
        for i in range(len(dates_list) - 1):
            from_date = dates_list[i]
            to_date = dates_list[i+1]
            access_token = authenticating_talkdesk(credentials, account_name)
            job_id = execute_report(access_token, report_name, from_date, to_date)
            report_is_created = check_loop(access_token, report_name, job_id)
            if report_is_created:
                response = download_report(access_token, report_name, job_id)
                delete_report(access_token, report_name, job_id)
                data = create_df(response)
                filter_ring_groups = report_config["filter_ring_groups"]
                if filter_ring_groups:
                    ring_groups_column = report_config["ring_groups_column"]
                    data = data[data[ring_groups_column].isin(filter_ring_groups)].copy()
                print(data)
                all_data.append(data)
        df = pd.concat(all_data)
        if report_name == "contacts" and info == "calls":
            transform_function = report_config["transform_function"]
            columns_to_load = report_config["columns_to_load"]
            rename_columns = report_config["rename_columns"]
            df_to_upload = transform_function(df, columns_to_load, rename_columns)
            print(df_to_upload)
        
        elif report_name == "studio_flow_execution" and info == "ivr":
            flow_column = report_config["flow_column"]
            flow_name = report_config["flow_name"]
            timestamp_column = report_config["timestamp_column"]
            df = df[df[flow_column] == flow_name].copy()
            df[timestamp_column] = pd.to_datetime(df[timestamp_column])
            df["started_at_utc"] = df.groupby("Interaction_ID")[timestamp_column].transform("min")
            df["started_at_utc"] = pd.to_datetime(df["started_at_utc"])
            min_date = min(df["started_at_utc"].dt.date)
            max_date = max(df["started_at_utc"].dt.date)
            contacts = generate_contacts_data(min_date, max_date)
            transform_function = report_config["transform_function"]
            agent_options = report_config["agent_options"]
            categories = report_config["categories"]
            ss_audios = report_config["ss_audios"]
            df_to_upload = transform_function(df, contacts, agent_options, categories, ss_audios)
            file_name_backup = f"src\jps\last_{report_name}_{info}_data_to_upload.csv"
            df_to_upload.to_csv(file_name_backup, index=False)
            print(df_to_upload)
        
        elif report_name == "studio_flow_execution" and info == "chat":
            flow_column = report_config["flow_column"]
            flow_name = report_config["flow_name"]
            timestamp_column = report_config["timestamp_column"]
            transform_function = report_config["transform_function"]
            escalations = report_config["escalations"]
            subs_to_replace = report_config["subs_to_replace"]
            df_to_upload = transform_function(df, flow_column, flow_name, timestamp_column, escalations, subs_to_replace)
            df_to_upload.to_csv(f"src\jps\last_{report_name}_{info}_data_to_upload.csv", index=False)
            print(df_to_upload)
            
        if insert_mode == "delete_insert":
            delete_keys = report_config["delete_keys"]
            dbutils.perform_safe_delete_insert_with_keys(conn, delete_keys, df_to_upload, schema, table_name)
            
    except ValueError as e:
        print(f"Oh no! Something went wrong: {e}")
        print(f"Please ignore if MAX date is today's date. We already have that info in the database!")



def main(optional: list):
    """ Runs the extract_transform_and_load_data function.
    Args:
        optional (int): Run mode.
    """

    match optional[0]:
        case 1:
            extract_transform_and_load_data("contacts", "calls")
        case 2:
            extract_transform_and_load_data("studio_flow_execution", "ivr")
        case 3:
            extract_transform_and_load_data("studio_flow_execution", "chat")