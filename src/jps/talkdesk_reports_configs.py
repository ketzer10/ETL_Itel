from src.jps.talkdesk_transform_functions import *


reports_configs = {
    "studio_flow_execution": {
        "ivr": {
            "schema": "jps",
            "table_name": "talkdesk_ivr_studio",
            "insert_mode": "delete_insert",
            "delete_keys": ["started_at_utc", "interaction_id"],
            "flow_column": "Flow Name",
            "flow_name": "JPS Main Flow - PROD",
            "timestamp_column": "Timestamp",
            "filter_ring_groups": False,
            "ss_audios": [
                'A 1_2 - Disconnect No Outage',
                    'A 1_3 Disconnect No Outage',
                    'A 2_2 - Disconnect No Outage',
                    'A 2_3 - Disconnect No Outage',
                    'A 3_3 - Disconnect No Outage',
                    'A7 - Disconnect No Outage - X Acc',
                    'A7 - Disconnected + Outage X Accoun',
                    'A7 - Has Outage -  X Account',
                    'A7 - Has Outage - X Account',
                    'A7 - Output - X Account details',
                    'A7 Output - 1_1 Account',
                    'A9 - Disconnect No Outage 1 Acc',
                    'A9 - Output 1_1 Account',
                    'Account 1_2 Output',
                    'Account 1_3 - Output',
                    'Account 2_2 Output',
                    'Account 2_3 - Output',
                    'Account 3_3 - Output',
                    'Audio 7  - No accounts found'
                    ],
            "agent_options": [
                "3 Speak with agent", "1 Speak with agent", "1 Voucher queries", "2 Go to Agent",
                    "1 Report a fire, broken pole or broken wire", "2 Speak with agent", "5 speak with a live agent"
                    ],
            "categories": {
                "1 Account related queries" : ["1 Bill Balance", "2 Reconnection",
                                                "3 Payment Hold", "4 Billing Queries"],
            
                    "2 Prepaid queries and requests" : ["1 Voucher queries", "2 Emergency top-up", 
                                                        "3 Payment Reversal transfers", "4 Top-up locations"],
            
                    "3 Report an emergency or an outage" : ["1 Report a fire, broken pole or broken wire", "2 Hear current outages",
                                                            "3 Report a new outage"],
            
                    "4 All other queries" : ["1 how to open an account", "2 report an illegal connection", 
                                            "3 report a defective streetlight", "4 general queries",
                                            "5 speak with a live agent", "6 return to the main menu"]
                            },
            "transform_function": transform_studio_ivr_data,
        },
        "chat": {
            "schema": "jps",
            "table_name": "talkdesk_chat_studio",
            "insert_mode": "delete_insert",
            "delete_keys": ["started_at_utc", "interaction_id"],
            "flow_column": "Flow Name",
            "flow_name": "JPS Live Chat - PROD",
            "timestamp_column": "Timestamp",
            "filter_ring_groups": False,
            "escalations": [
                "Bill & Balance query", "All other query", "Outage report & query",
                "Apply or Terminate Service", "no-match"
                ],
            "subs_to_replace": {
                "Bill & Balance query": "Bill & Balance",
                "All other query": "All other queries",
                "Outage report & query": "Outage report",
                "no-match": "No option selected"
            },
            "transform_function": transform_studio_chat_data,
        }
       
    },
    "contacts": {
        "calls": {
            "schema": "jps",
            "table_name": "talkdesk_calls_contacts",
            "insert_mode": "delete_insert",
            "delete_keys": ["started_at_utc", "contact_id"],
            "ring_groups_column": "Ring Groups",
            "filter_ring_groups": [
                "jps night emergency", "jps rewards", "jps_business",
                "jps_emergency", "jps_nightemergencies", "jps_rewards"
                ],
            "columns_to_load": [
                "Interaction ID", "Contact ID", "Phone Display Name", "Direction",
                "Contact Type", "Started At", "Ring Groups"
                ],
            "rename_columns": {"started_at": "started_at_utc"},
            "transform_function": transform_contacts_data
        }
    }
}