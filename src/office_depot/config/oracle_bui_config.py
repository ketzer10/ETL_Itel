from src.office_depot.functions.oracle_bui_functions import *

configs = {
    "general": {
        "new_columns_names": {
            "for_errors": ["report_name", "reference", "session_id", "date", "queue", "site", "agent_name"],
            "for_incidents": ["report_name", "date", "queue", "site", "agent_name", "incidents_qty"]
            },
        "delete_keys": ["report_name", "date"]
    },
    "Cisco_BUI_Oracle_assigned": {
        "sharepoint_config_key": "od_oracle_bui_assigned",
        "skiprows": 2,
        "skip_last_rows": False,
        "num_columns": 17,
        "extract_date_from_file_name_function": False,
        "need_sessionid_column": False,
        "columns_to_use": ["Reference", "SessionID", "DateCreated", "Queue", "SiteName", "CiscoAgentName"],
        "site_column": "SiteName",
        "itel_references": ["Itel - GY"],
        "agent_column": "CiscoAgentName",
        "date_column": "DateCreated",
        "get_agent_name_function": get_agent_name_from_email
    },
    "Dir_Phone_Agents_no_using_Order_Lookup": {
        "sharepoint_config_key": "od_oracle_bui_dir_phone_no_order_lookup",
        "skiprows": 1,
        "skip_last_rows": False,
        "num_columns": 12,
        "extract_date_from_file_name_function": False,
        "need_sessionid_column": False,
        "columns_to_use": ["Reference", "SressionID", "DateCreated", "QueueID", "SiteName", "AgentName"],
        "site_column": "SiteName",
        "itel_references": ["Itel - GY"],
        "agent_column": "AgentName",
        "date_column": "DateCreated",
        "get_agent_name_function": False
    },
    "Incidents_Cisco_BUI_Invalid_Email": {
        "sharepoint_config_key": "od_oracle_bui_incidents_created_invalid_email",
        "skiprows": 1,
        "skip_last_rows": False,
        "num_columns": 14,
        "extract_date_from_file_name_function": False,
        "need_sessionid_column": False,
        "columns_to_use": ["Reference", "SessionID", "DateCreated", "Queue", "SiteName", "AgentName"],
        "site_column": "SiteName",
        "itel_references": ["Itel - GY"],
        "agent_column": "AgentName",
        "date_column": "DateCreated",
        "get_agent_name_function": False
    },
    "ODPB_Email_Agents_no_using_Order_Lookup": {
        "sharepoint_config_key": "od_oracle_bui_odpb_email_no_order_lookup",
        "skiprows": 1,
        "skip_last_rows": False,
        "num_columns": 14,
        "extract_date_from_file_name_function": False,
        "need_sessionid_column": True,
        "columns_to_use": ["Reference", "SessionID", "DateRevised", "QueueID", "Location", "AgentFullName"],
        "site_column": "Location",
        "itel_references": ["Itel - GY"],
        "agent_column": "AgentFullName",
        "date_column": "DateRevised",
        "get_agent_name_function": False
    },
    "Sites_Agents_not_saving_the_incident": {
        "sharepoint_config_key": "od_oracle_bui_not_saving_the_incident",
        "skiprows": 1,
        "skip_last_rows": True,
        "num_columns": 5,
        "extract_date_from_file_name_function": extract_date_from_file_name,
        "need_sessionid_column": False,
        "columns_to_use": ["Date", "Queue", "Sites", "AgentName", "Incidents"],
        "site_column": "Sites",
        "itel_references": ["Itel - GY"],
        "agent_column": "AgentName",
        "date_column": "Date",
        "get_agent_name_function": get_agent_name_from_email
    }
}