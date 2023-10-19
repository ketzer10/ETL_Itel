# import packages
# from regex import P
import src.ancestry.functions.kgn_productivity_functions as kgn_productivity_functions
import src.ancestry.functions.kgn_productivity_kpi_dashboard_functions as kgn_productivity_kpi_dashboard_functions
import utils.utils as utils
import numpy as np

# extract configs from dshub_sharepoint
sh_config = utils.get_config("dshub_sharepoint_config")["folders"]


configs = {
    "agent_snapshop": {
        "folder_information": {
            "folder_id": sh_config["ancestry_kgn_productivity_agent_snapshot"]["id"],
            "folder_historical_id": sh_config["ancestry_kgn_productivity_agent_snapshot"]["historical_id"],
        },
        "save_information": {
            "delete_keys": ["date", "agent_name", "team_name"],
            "schema": sh_config["ancestry_kgn_productivity_agent_snapshot"]["schema"],
            "target_table": sh_config["ancestry_kgn_productivity_agent_snapshot"]["target_table"],
        },
        "read_information": {
            "read_with_dtype": {
                "Date": object, 
                "Agent Name": str, 
                "Team Name": str, 
                "Location Name": str,
                "Login Time": str, 
                "Agent Offered": object, 
                "Refused": object,	
                "Transferred": object,
                "Agent Abandons": object, 
                "Handled": object, 
                "Handle Time": str,
                "Active Talk Time": str,
                "Hold Time": str,
                "ACW Time": str,
                "Available Time": str,
                "Routing Time": str,
                "Occupancy": object
            }
        },
        "info_transform_function": {
           "df_handling": {
               "order_columns": [
                    "Date",
                    "Agent Name", 
                    "Team Name", 
                    "Location Name",
                    "Login Time", 
                    "Agent Offered",
                    "Refused",	
                    "Transferred",
                    "Agent Abandons",
                    "Handled",
                    "Handle Time",
                    "Active Talk Time",
                    "Hold Time",
                    "ACW Time",
                    "Available Time",
                    "Routing Time",
                    "Occupancy"
                ],
                "rename_columns": {
                    "Date": "date", 
                    "Agent Name": "agent_name", 
                    "Team Name": "team_name", 
                    "Location Name": "location_name",
                    "Login Time": "login_time_sec", 
                    "Agent Offered": "agent_offered", 
                    "Refused": "refused",	
                    "Transferred": "transferred",
                    "Agent Abandons": "agent_abandons", 
                    "Handled": "handled", 
                    "Handle Time": "handle_time_sec",
                    "Active Talk Time": "active_talk_time_sec",
                    "Hold Time": "hold_time_sec",
                    "ACW Time": "acw_time_sec",
                    "Available Time": "available_time_sec",
                    "Routing Time": "routing_time_sec",
                    "Occupancy": "occupancy"
                },
                "replace_values_in_columns": [
                    {
                        "columns": [
                            "occupancy"
                        ],
                        "replace_this": "%",
                        "for_this": ""
                    },
                    {
                        "columns": [
                            "occupancy"
                        ],
                        "replace_this": "",
                        "for_this": ""
                    },
                ],
                "validate_date_columns": {
                    "columns": ["date"],
                    "parameters": {
                        "date_format": "%Y/%m/%d"
                    }
                },
                "validate_text_columns": [
                    "agent_name", 
                    "team_name", 
                    "location_name"
                ],
                "validate_float_columns": [
                    "occupancy"
                ],
                "validate_int_columns": [
                    "agent_offered", 
                    "refused",	
                    "transferred",
                    "agent_abandons", 
                    "handled"
                ],
                "validate_duration_columns": {
                    "columns": [
                        "login_time_sec",
                        "handle_time_sec", 
                        "active_talk_time_sec",
                        "hold_time_sec",
                        "acw_time_sec",
                        "available_time_sec",
                        "routing_time_sec"
                    ],
                    "parameters": {
                        "regex": "(^\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)"
                    }
                },

           }
        },
        "transform_function": kgn_productivity_functions.transform_function_agent_snapshot
    },
    "agent_time_card":{
        "folder_information": {
            "folder_id": sh_config["ancestry_kgn_productivity_agent_time_card"]["id"],
            "folder_historical_id": sh_config["ancestry_kgn_productivity_agent_time_card"]["historical_id"],
        },
        "save_information": {
            "delete_keys": ["date","agent_session"],
            "schema": sh_config["ancestry_kgn_productivity_agent_time_card"]["schema"],
            "target_table": sh_config["ancestry_kgn_productivity_agent_time_card"]["target_table"],
        },
        "read_information": {
            "read_with_dtype": {
                "Agent Name (ID)": str,
                "Agent Session": str,
                "Login Date": object,
                "Logout Date": object,
                "Duration": str
            }
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "Date",
                    "Team Name (ID)",
                    "team_name_id",
                    "Agent Name (ID)",
                    "agent_id",
                    "Agent Session",
                    "Login Date",
                    "Logout Date",
                    "Duration",
                    "duration_sec"
                ],
                "rename_columns": {
                    "Date": "date",
                    "Team Name (ID)": "team_name",
                    "Agent Name (ID)": "agent_name",
                    "Agent Session": "agent_session",
                    "Login Date": "login_date",
                    "Logout Date": "logout_date",
                    "Duration": "duration"
                },
                # "validate_duration_columns": {
                #     "columns": [
                #         "duration_sec"
                #     ],
                #     "parameters": {
                #         "regex": "(^\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)"
                #     }
                # },
                "validate_date_columns": {
                    "columns": [
                        "date"
                    ],
                    "parameters": {
                        "date_format": "%m.%d.%Y"
                    }
                },
                "validate_datetime_columns": {
                    "columns": [
                        "login_date",
                        "logout_date"
                    ],
                    "parameters": {
                        "date_format": "%m/%d/%y %H:%M:%S"
                    }
                },
                "validate_text_columns": [
                    "team_name", "team_name_id", "agent_name", "agent_id", "agent_session", "duration"
                ],
                "validate_int_columns": [
                    "duration_sec"
                ]
            }
        },
        "transform_function": kgn_productivity_functions.transform_function_agent_time_card
    },
    "coaching_fs_meeting": {
        "folder_information": {
            "folder_id": sh_config['ancestry_kgn_productivity_coaching_fs_meeting']['id'],
            "folder_historical_id": sh_config['ancestry_kgn_productivity_coaching_fs_meeting']['historical_id']
        },
        "save_information": {
            "delete_keys": ["date", "record_id"],
            "schema": sh_config['ancestry_kgn_productivity_coaching_fs_meeting']['schema'],
            "target_table": sh_config['ancestry_kgn_productivity_coaching_fs_meeting']['target_table']
        },
        "read_information": {
            "read_with_dtype": {
                "Duration": str,
                "Date": object,
                "Start": object,
                "End": object,
                "Record ID": str,
                "Approver Name": str,
                "Agent Name": str,
                "Log out reason": str
            }
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "Record ID",
                    "Approver Name",
                    "Agent Name",
                    "Log out reason",
                    "Start",
                    "End",
                    "Duration",
                    "Date"
                ],
                "rename_columns": {
                    "Record ID": "record_id",
                    "Approver Name": "approver_name",
                    "Agent Name": "agent_name",
                    "Log out reason": "log_out_reason",
                    "Start": "start_time",
                    "End": "end_time",
                    "Duration": "duration_sec",
                    "Date": "date"
                },
                "validate_duration_columns": {
                    "columns": [
                        "duration_sec"
                    ],
                    "parameters": {
                        "regex": "(^\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)"
                    }
                },
                "validate_date_columns": {
                    "columns": [
                        "date"
                    ],
                    "parameters": {
                        "date_format": "%m/%d/%Y"
                    }
                },
                "validate_datetime_columns": {
                    "columns": [
                        "start_time",
                        "end_time"
                    ],
                    "parameters": {
                        "date_format": "%H:%M:%S"
                    }
                },
                "validate_text_columns": [
                    "record_id",
                    "approver_name",
                    "agent_name",
                    "log_out_reason"
                ]
            }
        },
        "transform_function": kgn_productivity_functions.transform_function_coaching_fs_meeting
    },
    "sys_issues": {
        "folder_information": {
            "folder_id": sh_config['ancestry_kgn_productivity_sys_issues']['id'],
            "folder_historical_id": sh_config['ancestry_kgn_productivity_sys_issues']['historical_id']
        },
        "save_information": {
            "delete_keys": ["date", "record_id"],
            "schema": sh_config['ancestry_kgn_productivity_sys_issues']['schema'],
            "target_table": sh_config['ancestry_kgn_productivity_sys_issues']['target_table']
        },
        "read_information": {
            "read_with_dtype": {
                "Duration ": "str",
                "Date ": "datetime64",
                "Start ": "str",
                "End": "str",
                "Record ID": "str",
                "Being Logged by": "str",
                "Approver Name": "str",
                "Agent name": "str",
                "Agent Supervisor": "str",
                "Ticket Number": "str",
                "Client or Vendor Related": "str",
                "Issue Description": "str"
            }
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "Record ID",
                    "Being Logged by",
                    "Approver Name",
                    "Agent name",
                    "Agent Supervisor",
                    "Ticket Number",
                    "Client or Vendor Related",
                    "Issue Description",
                    "Start ",
                    "End",
                    "Duration ",
                    "Date "
                ],
                "rename_columns": {
                    "Record ID": "record_id",
                    "Being Logged by": "being_logged_by",
                    "Approver Name": "approver_name",
                    "Agent name": "agent_name",
                    "Agent Supervisor": "agent_supervisor",
                    "Ticket Number": "ticket_number",
                    "Client or Vendor Related": "client_or_vendor_related",
                    "Issue Description": "issue_description",
                    "Start ": "start_time",
                    "End": "end_time",
                    "Duration ": "duration_sec",
                    "Date ": "date"
                },
                "validate_duration_columns": {
                    "columns": [
                        "duration_sec"
                    ],
                    "parameters": {
                        "regex": "(^\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)"
                    }
                },
                "validate_date_columns": {
                    "columns": [
                        "date"
                    ],
                    "parameters": {
                        "date_format": "%m/%d/%Y"
                    }
                },
                "validate_datetime_columns": {
                    "columns": [
                        "start_time",
                        "end_time"
                    ],
                    "parameters": {
                        "date_format": "%H:%M:%S"
                    }
                },
                "validate_text_columns": [
                    "record_id",
                    "being_logged_by",
                    "approver_name",
                    "agent_name",
                    "agent_supervisor",
                    "ticket_number",
                    "client_or_vendor_related",
                    "issue_description"
                ]
            }
        },
        "transform_function": kgn_productivity_functions.transform_function_sys_issues
    },
    "unavailable_time": {
        "folder_information": {
            "folder_id": sh_config['ancestry_kgn_productivity_unavailable_time']['id'],
            "folder_historical_id": sh_config['ancestry_kgn_productivity_unavailable_time']['historical_id']
        },
        "save_information": {
            "delete_keys": ["agent_name","date","code"],
            "schema": sh_config['ancestry_kgn_productivity_unavailable_time']['schema'],
            "target_table": sh_config['ancestry_kgn_productivity_unavailable_time']['target_table']
        },
        "read_information": {
            "read_with_dtype": {
                "Date": object,
                "Duration": "str",
                "DurationInSeconds": "int64",
                "Percent": "float64",
                "Agent Name (ID)": "str",
                "Code": "str",
                "Code Type": "str"
            }
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "Date",
                    "id",
                    "Agent Name (ID)",
                    "Code",
                    "Code Type",
                    "Duration",
                    "DurationInSeconds",
                    "Percent"
                ],
                "rename_columns": {
                    "Date":  "date",
                    "Agent Name (ID)": "agent_name",
                    "Code": "code",
                    "Code Type": "code_type",
                    "Duration": "duration",
                    "DurationInSeconds": "duration_sec",
                    "Percent": "pct"
                },
                "validate_int_columns": [
                    "duration_sec"
                ],
                "validate_float_columns": [
                    "pct"
                ],
                "validate_text_columns": [
                    "id",
                    "agent_name",
                    "code",
                    "code_type",
                    "duration"
                ],
                "validate_date_columns": {
                    "columns": [
                        "date"
                    ],
                    "parameters": {
                        "date_format": "%m.%d.%Y"
                    }
                }
            }
        },
        "transform_function": kgn_productivity_functions.transform_function_unavailable_time
    },
    "qa": {
        "folder_information": {
            "folder_id": sh_config['ancestry_kgn_productivity_qa']['id'],
            "folder_historical_id": sh_config['ancestry_kgn_productivity_qa']['historical_id']
        },
        "save_information": {
            "delete_keys": ["date", "agent", "workflow_instance_id"],
            "schema": sh_config['ancestry_kgn_productivity_qa']['schema'],
            "target_table": sh_config['ancestry_kgn_productivity_qa']['target_table']
        },
        "read_information": {
            "read_with_dtype": {
                "AGENT": "str",
                "TEAM": "str",
                "WORKFLOW TYPE": "str",
                "DISPLAY STATUS": "str",
                "WORKFLOWINSTANCE ID": "str",
                "PLAN NAME": "str",
                "FORM NAME": "str",
                "EVALUATOR": "str",
                "AVERAGE SCORE": "float64",
                "CHANNEL TYPE": "str",
                "INTERACTION DATE": "datetime64",
                "INTERACTION DURATION": "str",
            }
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "AGENT",
                    "TEAM",
                    "WORKFLOW TYPE",
                    "DISPLAY STATUS",
                    "WORKFLOWINSTANCE ID",
                    "PLAN NAME",
                    "FORM NAME",
                    "EVALUATOR",
                    "AVERAGE SCORE",
                    "CHANNEL TYPE",
                    "INTERACTION DATE",
                    "INTERACTION DURATION"
                ],
                "rename_columns": {
                    "AGENT": "agent",
                    "TEAM": "team",
                    "WORKFLOW TYPE": "workflow_type",
                    "DISPLAY STATUS": "display_status",
                    "WORKFLOWINSTANCE ID": "workflow_instance_id",
                    "PLAN NAME": "plan_name",
                    "FORM NAME": "form_name",
                    "EVALUATOR": "evaluator",
                    "AVERAGE SCORE": "average_score",
                    "CHANNEL TYPE": "channel_type",
                    "INTERACTION DATE": "date",
                    "INTERACTION DURATION": "interaction_duration_sec",
                },
                "validate_date_columns": {
                    "columns": [
                        "date"
                    ],
                    "parameters": {
                        "date_format": "%d %b, %Y"
                    }
                },
                "validate_float_columns": [
                    "average_score"
                ],
                "validate_text_columns": [
                    "agent", "team", "workflow_type", "display_status", 
                    "workflow_instance_id", "plan_name", "form_name",
                    "evaluator", "channel_type"
                ],
                "validate_duration_columns": {
                    "columns": [
                        "interaction_duration_sec"
                    ],
                    "parameters": {
                        "regex": "(^\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)" 
                    }
                }
            }
        },
        "transform_function": kgn_productivity_kpi_dashboard_functions.transform_function_qa
    },
    "csat": {
        "folder_information": {
            "folder_id": sh_config['ancestry_kgn_productivity_csat']['id'],
            "folder_historical_id": sh_config['ancestry_kgn_productivity_csat']['historical_id']
        },
        "save_information": {
            "delete_keys": ["date", "agent"],
            "schema": sh_config['ancestry_kgn_productivity_csat']['schema'],
            "target_table": sh_config['ancestry_kgn_productivity_csat']['target_table']
        },
        "read_information": {
            "read_with_dtype": {
                "Email": "str",
                "Custom Employee Id": "str",
                "Name": "str",
                "Requests": object,
                "Responses": object,
                "Percent Positive": object,
                "vs prev 1 days": object,
                "Percent Negative":object,
                "vs prev 1 days": object,
                "Percent Resolved": object,
                "vs prev 1 days": object,
                "Total": object,
                "Clarity": object,
                "Empathy": object,
                "Friendliness": object,
                "Knowledge": object,
                "Problem Solving": object,
                "Professionalism": object,
                "Total": object,
                "Efficient": object,
                "Empathetic": object,
                "Friendly": object,
                "Helpful": object,
                "Knowledgeable": object,
                "Professional": object,
                "Reviews": object,
                "Avg. Score": object,
                "Annotations": object
            }
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "date",
                    "Email",
                    "Name",
                    "Requests",
                    "Responses",
                    "Percent Positive",
                    "Percent Negative",
                    "Percent Resolved",
                    # one slot of evaluation
                    "Clarity",
                    "Empathy",
                    "Friendliness",
                    "Knowledge",
                    "Problem Solving",
                    "Professionalism",
                    # second slot of evaluation
                    "Efficient",
                    "Empathetic",
                    "Friendly", 
                    "Helpful",
                    "Knowledgeable",
                    "Professional",
                ],
                "rename_columns": {
                    "Email": "email",
                    "Name": "agent",
                    "Requests": "requests",
                    "Responses": "responses",
                    "Percent Positive": "percent_positive",
                    "Percent Negative": "percent_negative",
                    "Percent Resolved": "percent_resolved",
                    "Clarity": "clarity",
                    "Empathy": "empathy",
                    "Friendliness": "friendliness",
                    "Knowledge": "knowledge",
                    "Problem Solving": "problem_solving",
                    "Professionalism": "professionalism",
                    "Efficient": "efficient",
                    "Empathetic": "empathetic",
                    "Friendly": "friendly",
                    "Helpful": "helpful",
                    "Knowledgeable": "knowledgeable",
                    "Professional": "professional"
                },
                "replace_values_in_columns": [
                    {
                        "columns": ["percent_positive", "percent_negative", "percent_resolved"],
                        "replace_this": "%",
                        "for_this": ""
                    }
                ],
                "validate_date_columns": {
                    "columns": [
                        "date"
                    ],
                    "parameters": {
                        "date_format": "%Y-%m-%d"
                    }
                },
                "validate_float_columns": [
                    "percent_positive", "percent_negative", "percent_resolved"
                ],
                "validate_text_columns": [
                    "agent", "email"
                ],
                "validate_int_columns": [
                    "requests", "responses", 
                    "clarity", "empathy", "friendliness", "knowledge", "problem_solving", "professionalism",
                    "efficient", "empathetic", "friendly", "helpful", "knowledgeable", "professional"
                ]
            }
        },
        "transform_function": kgn_productivity_kpi_dashboard_functions.transform_function_csat
    }
}
    



















