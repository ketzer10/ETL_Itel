# import packages
# from regex import P
import src.louis_vuitton.functions.kpi_dashboard_functions as lv_kpi_dashboard_functions
import utils.utils as utils

# extract configs from dshub_sharepoint
sh_config = utils.get_config("dshub_sharepoint_config")["folders"]


configs = {
    "lv_glb_percent_on_queve": {
        "folder_information": {
            "folder_id": sh_config['lv_glb_percent_on_queve']['id'],
            "folder_historical_id": sh_config['lv_glb_percent_on_queve']['historical_id']
        },
        "save_information": {
            "delete_keys": ["date", "agent_name"],
            "schema": sh_config['lv_glb_percent_on_queve']['schema'],
            "target_table": sh_config['lv_glb_percent_on_queve']['target_table']
        },
        "read_information": {
            "read_with_dtype": {
                "User Name": "str",
                "Date": "datetime64",
                "Login": "datetime64",
                "Logout": "datetime64",
                "Online": "str",
                "Off Queue": "str",
                "Unnamed: 8": "float64",
                "On Queue": "str",
                "Unnamed: 12": "float64",
                "Interacting": "str",
                "Unnamed: 14": "float64",
                "Idle": "str",
                "Unnamed: 16": "float64",
                "Not Responding": "str",
                "Unnamed: 18": "float64",
                "Total ACD": "str"
            }
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "User Name",
                    "Date",
                    "Login",
                    "Logout",
                    "Online",
                    "Off Queue",
                    "Unnamed: 8",
                    "On Queue",
                    "Unnamed: 12",
                    "Interacting",
                    "Unnamed: 14",
                    "Idle",
                    "Unnamed: 16",
                    "Not Responding",
                    "Unnamed: 18",
                    "Total ACD"
                ],
                "rename_columns": {
                    "User Name": "agent_name",
                    "Date": "date",
                    "Login": "login",
                    "Logout": "logout",
                    "Online": "online_sec",
                    "Off Queue": "off_queue_sec",
                    "Unnamed: 8": "off_queue_pct",
                    "On Queue": "on_queue_sec",
                    "Unnamed: 12": "on_queue_pct",
                    "Interacting": "interacting_sec",
                    "Unnamed: 14": "interacting_pct",
                    "Idle": "idle_sec",
                    "Unnamed: 16": "idle_pct",
                    "Not Responding": "not_responding_sec",
                    "Unnamed: 18": "not_responding_pct",
                    "Total ACD": "total_acd_sec"
                },
                "validate_duration_columns": {
                    "columns": [
                        "online_sec", "off_queue_sec", "on_queue_sec", 
                        "interacting_sec", "idle_sec", "not_responding_sec",
                        "total_acd_sec"
                    ],
                    "parameters": {
                        "regex": "(^\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)"
                    }
                }
            }
        },
        "transform_function": lv_kpi_dashboard_functions.transform_function_percent_on_queve
    },
    "lv_glb_quality_assessment": {
        "folder_information": {
            "folder_id": sh_config['lv_glb_quality_assessment']['id'],
            "folder_historical_id": sh_config['lv_glb_quality_assessment']['historical_id']
        },
        "save_information": {
            "delete_keys": ["id", "date"],
            "schema": sh_config['lv_glb_quality_assessment']['schema'],
            "target_table": sh_config['lv_glb_quality_assessment']['target_table']
        },
        "read_information": {
            "read_with_dtype": {
                "ID": "str", 
                "Start time": "datetime64", 
                "Completion time": "datetime64", 
                "Email": "str", 
                "Name": "str", 
                "Team Manager": "str",
                "Call Type2": "str", 
                "Month": "str", 
                "Date": "datetime64", 
                "QA By": "str", 
                "Inbound Phone #": "str",
                "Recording Date / Time": "str",
                "Duration": "str", 
                "Batch #": "int64",
                "Baseline Job Requirement is 90%": "float64",
            }
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "ID", 
                    "Start time", 
                    "Completion time", 
                    "Email", 
                    "Name", 
                    "Team Manager",
                    "Call Type2", 
                    "Month", 
                    "Date", 
                    "QA By", 
                    "Inbound Phone #",
                    "Recording Date / Time",
                    "Duration", 
                    "Batch #",
                    "Baseline Job Requirement is 90%"
                ],
                "rename_columns": {
                    "ID": "id", 
                    "Start time": "start_time", 
                    "Completion time": "completion_time", 
                    "Email": "email", 
                    "Name": "name", 
                    "Team Manager": "team_manager",
                    "Call Type2": "call_type_two", 
                    "Month": "month", 
                    "Date": "date", 
                    "QA By": "qa_by", 
                    "Inbound Phone #": "inbound_phone",
                    "Recording Date / Time": "recording_date_time",
                    "Duration": "duration", 
                    "Batch #": "batch",
                    "Baseline Job Requirement is 90%": "base_job_requirement",
                },
                # "validate_duration_columns": {
                #     "columns": [
                #         "online_sec", "off_queue_sec", "on_queue_sec", 
                #         "interacting_sec", "idle_sec", "not_responding_sec",
                #         "total_acd_sec"
                #     ],
                #     "parameters": {
                #         "regex": "(^\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)"
                #     }
                # }
            }
        },
        "transform_function": lv_kpi_dashboard_functions.transform_function_quality_assessment
    },
    "lv_glb_service_level_requirement": {
        "folder_information": {
            "folder_id": sh_config['lv_glb_service_level_requirement']['id'],
            "folder_historical_id": sh_config['lv_glb_service_level_requirement']['historical_id']
        },
        "save_information": {
            "delete_keys": ["date"],
            "schema": sh_config['lv_glb_service_level_requirement']['schema'],
            "target_table": sh_config['lv_glb_service_level_requirement']['target_table']
        },
        "read_information": {
            "read_with_dtype": {
                "Date": object, 
                "Offered": "float64", 
                "Answered": "float64", 
                "Abandoned": "float64", 
                "Abandon %": "float64", 
                "Service Level %": "float64",
                "ASA": "str", 
                "Avg Talk": "str", 
                "Avg ACW": "str", 
                "AHT": "str", 
                "Avg Hold": "str",
                "Transferred": "float64",
                "Transfer %": "float64",
            }
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "Date", 
                    "Offered",
                    "Answered",
                    "Abandoned",
                    "Abandon %", 
                    "Service Level %",
                    "ASA",
                    "Avg Talk",
                    "Avg ACW",
                    "AHT", 
                    "Avg Hold",
                    "Transferred",
                    "Transfer %",
                ],
                "rename_columns": {
                    "Date": "date", 
                    "Offered": "offered", 
                    "Answered": "answered", 
                    "Abandoned": "abandoned", 
                    "Abandon %": "abandon_pct", 
                    "Service Level %": "service_level_pct",
                    "ASA": "asa", 
                    "Avg Talk": "avg_talk", 
                    "Avg ACW": "avg_acw", 
                    "AHT": "aht", 
                    "Avg Hold": "avg_hold",
                    "Transferred": "transferred",
                    "Transfer %": "transfer_pct",
                },
                "validate_duration_columns": {
                    "columns": [
                        "asa", "avg_talk", "avg_acw", 
                        "aht", "avg_hold", 
                    ],
                    "parameters": {
                        "regex": "(^\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)"
                    }
                }
            }
        },
        "transform_function": lv_kpi_dashboard_functions.transform_function_service_level_requirement
    },
    "lv_glb_client_report": {
        "folder_information": {
            "folder_id": sh_config['lv_glb_client_report']['id'],
            "folder_historical_id": sh_config['lv_glb_client_report']['historical_id']
        },
        "save_information": {
            "delete_keys": ["date", "genesys_id"],
            "schema": sh_config['lv_glb_client_report']['schema'],
            "target_table": sh_config['lv_glb_client_report']['target_table']
        },
        "read_information": {
            "read_with_dtype": {
                "Sr. Manager": "str", 
                "Team Manager": "str", 
                "Client Advisor": "str", 
                "Email": "str",
                "Genesys ID": "str",
                "NEMO code": "str",
                "Specialty": "str",
                "Exit/LOA": "str",
                "Rotation Group": "str",
                "Location": "str",
                "FT/PT": "str",
                "Hire Date": "datetime64",
                "Tenure (Days)": "float64",
                "Calls Handled": "str",
                "CPH (On Queue)": "str", 
                "Avg Handle Time (min)": "str", 
                "Avg Hold Time (min)": "str",
                "Avg ACW (min)": "str", 
                "Sales (k)": "str", 
                "% On Queue/Logged In": "float64", 
                "Sales % Weekly Target": "float64", 
                "Conversion": "float64",
                "Transactions": "str",
                "MyCR Created": "str",
            }
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "date",
                    "Sr. Manager", 
                    "Team Manager", 
                    "Client Advisor", 
                    "Email",
                    "Genesys ID",
                    "NEMO code",
                    "Specialty",
                    "Exit/LOA",
                    "Rotation Group",
                    "Location",
                    "FT/PT",
                    "Hire Date",
                    "Tenure (Days)",
                    "Calls Handled",
                    "CPH (On Queue)", 
                    "Avg Handle Time (min)", 
                    "Avg Hold Time (min)",
                    "Avg ACW (min)", 
                    "Sales (k)", 
                    "% On Queue/Logged In", 
                    "Sales % Weekly Target", 
                    "Conversion",
                    "Transactions",
                    "MyCR Created",
                ],
                "rename_columns": {
                    "Sr. Manager": "manager", 
                    "Team Manager": "team_manager", 
                    "Client Advisor": "client_advisor", 
                    "Email": "email",
                    "Genesys ID": "genesys_id",
                    "NEMO code": "nemo_code",
                    "Specialty": "specialty",
                    "Exit/LOA": "exit_qa",
                    "Rotation Group": "rotation_group",
                    "Location": "location_",
                    "FT/PT": "ft_pt",
                    "Hire Date": "hire_date",
                    "Tenure (Days)": "ternure",
                    "Calls Handled": "calls_handled",
                    "CPH (On Queue)": "cph_on_queue", 
                    "Avg Handle Time (min)": "avg_handle_time_min", 
                    "Avg Hold Time (min)": "avg_hold_time_min",
                    "Avg ACW (min)": "avg_acw_min", 
                    "Sales (k)": "sales_k", 
                    "% On Queue/Logged In": "on_queue_logged_in_pct", 
                    "Sales % Weekly Target": "sales_weekly_target_pct", 
                    "Conversion": "conversion",
                    "Transactions": "transactions",
                    "MyCR Created": "mycr_created",
                },
                "replace_values_in_columns": [
                    {
                        "columns": ["transactions", "calls_handled"],
                        "replace_this": "-",
                        "for_this": ""
                    }
                ],
                "validate_int_columns":  ["transactions", "calls_handled"]
            }
        },
        "transform_function": lv_kpi_dashboard_functions.transform_function_client_report
    }
}
    



















