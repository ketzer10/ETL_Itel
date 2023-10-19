configs = {
#    "handled_compliance_inbound":{
#        "info_transform_function_before":{
#            "int_columns": [],
#            "float_columns": [],
#            "date_columns": [],
#        },
#        "df_handling": {
#            "order_columns": [
#                "Interval (Day)", "Compliance (Met/ Not Met)", "Original Locks", "Forecast Adjustment", 
#                "Revised Locks", "Enterprise Offered %", "Vendor Compliance Goal", "Handled",
#                "Short Contacts", "Handled (w/o) Short Contacts", "Vendor Handled vs Compliance Goal",
#                "Digital Vendor Handled (%)", "AHT (s)",
#                "Digital HC%",
#            ],
#            "rename_columns": {
#                "Interval (Day)": "date", 
#                "Compliance (Met/ Not Met)": "compliance_met_not_met", 
#                "Original Locks": "original_locks", 
#                "Forecast Adjustment":  "forecast_adjustment", 
#                "Revised Locks": "revised_locks", 
#                "Enterprise Offered %": "enterprise_offered_pct", 
#                "Vendor Compliance Goal": "vendor_compliance_goal", 
#                "Handled": "handled",
#                "Short Contacts":  "short_contacts", 
#                "Handled (w/o) Short Contacts": "handled_w_o_short_contacts", 
#                "Vendor Handled vs Compliance Goal": "vendor_handled_vs_compliance_goal",
#                "Digital Vendor Handled (%)": "digital_vendor_handled_pct",
#                "AHT (s)": "aht_sec",
#                "Digital HC%": "digital_hc_pct",	
#            },
#            "validate_float_columns": [
#                "original_locks", "forecast_adjustment", "revised_locks", 
#                "enterprise_offered_pct", "vendor_compliance_goal", 
#                "handled", "short_contacts", "handled_w_o_short_contacts",
#                "vendor_handled_vs_compliance_goal", "digital_vendor_handled_pct", 
#                # "aht_sec", #"digital_hc_pct", 
#            ],
#            "validate_text_columns": [
#                "compliance_met_not_met"
#            ],
#            # "validate_date_columns": {
#            #     "columns": [
#            #         "date"                
#            #     ],
#            #     "parameters": {
#            #         "raise_flag": False,
#            #         "format": "%Y-%m-%d"
#            #     }
#            # }
#        },
#        "info_transform_function_affter":{
#            "date_columns": [],
#        },
#        "save_information":{
#            "keys": ["date", "call_type", "site"]
#        }
#    },
#    "handled_compliance_outbound":{
#        "info_transform_function_before":{
#            "int_columns": [],
#            "float_columns": [],
#            "date_columns": [],
#        },
#        "df_handling": {
#            "order_columns": [
#                "Interval (Day)", "Compliance (Met/ Not Met)", "Original Locks", "Forecast Adjustment", 
#                "Revised Locks", "Enterprise Offered %", "Vendor Compliance Goal", "Handled",
#                "Short Contacts", "Handled (w/o) Short Contacts", "Vendor Handled vs Compliance Goal",
#                "Digital Vendor Handled (%)", "AHT (s)",
#                "Digital HC%",
#            ],
#            "rename_columns": {
#                "Interval (Day)": "date", 
#                "Compliance (Met/ Not Met)": "compliance_met_not_met", 
#                "Original Locks": "original_locks", 
#                "Forecast Adjustment":  "forecast_adjustment", 
#                "Revised Locks": "revised_locks", 
#                "Enterprise Offered %": "enterprise_offered_pct", 
#                "Vendor Compliance Goal": "vendor_compliance_goal", 
#                "Handled": "handled",
#                "Short Contacts":  "short_contacts", 
#                "Handled (w/o) Short Contacts": "handled_w_o_short_contacts", 
#                "Vendor Handled vs Compliance Goal": "vendor_handled_vs_compliance_goal",
#                "Digital Vendor Handled (%)": "digital_vendor_handled_pct",
#                "AHT (s)": "aht_sec",
#                "Digital HC%": "digital_hc_pct",	
#            },
#            "validate_float_columns": [
#                "original_locks", "forecast_adjustment", "revised_locks", 
#                "enterprise_offered_pct", "vendor_compliance_goal", 
#                "handled", "short_contacts", "handled_w_o_short_contacts",
#                "vendor_handled_vs_compliance_goal", "digital_vendor_handled_pct", 
#                # "aht_sec", #"digital_hc_pct", 
#            ],
#            "validate_text_columns": [
#                "compliance_met_not_met"
#            ],
#            # "validate_date_columns": {
#            #     "columns": [
#            #         "date"                
#            #     ],
#            #     "parameters": {
#            #         "raise_flag": False,
#            #         "format": "%Y-%m-%d"
#            #     }
#            # }
#        },
#        "info_transform_function_affter":{
#            "date_columns": [],
#        },
#        "save_information":{
#            "keys": ["date", "call_type", "site"]
#        }
#    },
    "handled_compliance_outbound_jam":{
        "info_transform_function_before":{
            "int_columns": [],
            "float_columns": [],
            "date_columns": [],
        },
        "df_handling": {
            "order_columns": [
                "Time Interval",
                "Original Locks",
                "Revised Locks",
                "Compliance Goal",
                "Handled",
                "Handled w/o short contacts",
                "Handled vs Compl goal",
                "Vendor Handled%",
                "AHT"
            ],
            "rename_columns": {
                "Time Interval": "date", 
                "Original Locks": "original_locks", 
                "Revised Locks": "revised_locks", 
                "Compliance Goal":"vendor_compliance_goal",
                "Handled": "handled",
                "Handled w/o short contacts": "handled_w_o_short_contacts", 
                "Handled vs Compl goal": "vendor_handled_vs_compliance_goal",
                "Vendor Handled%": "digital_vendor_handled_pct",
                "AHT": "aht_sec",
            },
            "validate_float_columns": [
                "original_locks", "revised_locks",
                "handled", "handled_w_o_short_contacts",
                "vendor_handled_vs_compliance_goal", "digital_vendor_handled_pct"
                # "aht_sec", #"digital_hc_pct", 
            ],
        },
        "info_transform_function_affter":{
            "date_columns": [],
        },
        "save_information":{
            "keys": ["date", "call_type", "site"]
        }
    },
    "handled_compliance_inbound_jam":{
        "info_transform_function_before":{
            "int_columns": [],
            "float_columns": [],
            "date_columns": [],
        },
        "df_handling": {
            "order_columns": [
                "Week",
                "Intervals",
                "Passed Int",
                "SC%",
                "Time Interval",
                "Original Locks",
                "Revised Locks",
                "Compliance Goal",
                "Handled",
                "Handled w/o short contacts",
                "Handled vs Compl goal",
                "Vendor Handled%",
                "AHT"
            ],
            "rename_columns": {
                "Week":"week",
                "Intervals":"intervals",
                "Passed Int":"passed_int",
                "SC%":"sc_percent",
                "Time Interval": "date", 
                "Original Locks": "original_locks", 
                "Revised Locks": "revised_locks", 
                "Compliance Goal":"vendor_compliance_goal",
                "Handled": "handled",
                "Handled w/o short contacts": "handled_w_o_short_contacts", 
                "Handled vs Compl goal": "vendor_handled_vs_compliance_goal",
                "Vendor Handled%": "digital_vendor_handled_pct",
                "AHT": "aht_sec",
            },
            "validate_float_columns": [
                "original_locks", "revised_locks",
                "handled", "handled_w_o_short_contacts",
                "vendor_handled_vs_compliance_goal", "digital_vendor_handled_pct",
                "week","intervals","passed_int","sc_percent" 
                # "aht_sec", #"digital_hc_pct", 
            ],
        },
        "info_transform_function_affter":{
            "date_columns": [],
        },
        "save_information":{
            "keys": ["date", "call_type", "site"]
        }
    },
    "handled_compliance_outbound":{
        "info_transform_function_before":{
            "int_columns": [],
            "float_columns": [],
            "date_columns": [],
        },
        "df_handling": {
            "order_columns": [
                "Time Interval",
                "Original Locks",
                "Revised Locks",
                "Compliance Goal",
                "Handled",
                "Handled w/o short contacts",
                "Handled vs Compl goal",
                "Vendor Handled%",
                "AHT"
            ],
            "rename_columns": {
                "Time Interval": "date", 
                "Original Locks": "original_locks", 
                "Revised Locks": "revised_locks", 
                "Compliance Goal":"vendor_compliance_goal",
                "Handled": "handled",
                "Handled w/o short contacts": "handled_w_o_short_contacts", 
                "Handled vs Compl goal": "vendor_handled_vs_compliance_goal",
                "Vendor Handled%": "digital_vendor_handled_pct",
                "AHT": "aht_sec",
            },
            "validate_float_columns": [
                "original_locks", "revised_locks",
                "handled", "handled_w_o_short_contacts",
                "vendor_handled_vs_compliance_goal", "digital_vendor_handled_pct"
                # "aht_sec", #"digital_hc_pct", 
            ],
        },
        "info_transform_function_affter":{
            "date_columns": [],
        },
        "save_information":{
            "keys": ["date", "call_type", "site"]
        }
    },
    "handled_compliance_inbound":{
        "info_transform_function_before":{
            "int_columns": [],
            "float_columns": [],
            "date_columns": [],
        },
        "df_handling": {
            "order_columns": [
                "Week",
                "Intervals",
                "Passed Int",
                "SC%",
                "Time Interval",
                "Original Locks",
                "Revised Locks",
                "Compliance Goal",
                "Handled",
                "Handled w/o short contacts",
                "Handled vs Compl goal",
                "Vendor Handled%",
                "AHT"
            ],
            "rename_columns": {
                "Week":"week",
                "Intervals":"intervals",
                "Passed Int":"passed_int",
                "SC%":"sc_percent",
                "Time Interval": "date", 
                "Original Locks": "original_locks", 
                "Revised Locks": "revised_locks", 
                "Compliance Goal":"vendor_compliance_goal",
                "Handled": "handled",
                "Handled w/o short contacts": "handled_w_o_short_contacts", 
                "Handled vs Compl goal": "vendor_handled_vs_compliance_goal",
                "Vendor Handled%": "digital_vendor_handled_pct",
                "AHT": "aht_sec",
            },
            "validate_float_columns": [
                "original_locks", "revised_locks",
                "handled", "handled_w_o_short_contacts",
                "vendor_handled_vs_compliance_goal", "digital_vendor_handled_pct", 
                "week","intervals","passed_int","sc_percent" 
                # "aht_sec", #"digital_hc_pct", 
            ],
        },
        "info_transform_function_affter":{
            "date_columns": [],
        },
        "save_information":{
            "keys": ["date", "call_type", "site"]
        }
    },
    "handled_compliance_outbound_geo":{
        "info_transform_function_before":{
            "int_columns": [],
            "float_columns": [],
            "date_columns": [],
        },
        "df_handling": {
            "order_columns": [
                "Time Interval",
                "Original Locks",
                "Revised Locks",
                "Compliance Goal",
                "Handled",
                "Handled w/o short contacts",
                "Handled vs Compl goal",
                "Vendor Handled%",
                "AHT"
            ],
            "rename_columns": {
                "Time Interval": "date", 
                "Original Locks": "original_locks", 
                "Revised Locks": "revised_locks", 
                "Compliance Goal":"vendor_compliance_goal",
                "Handled": "handled",
                "Handled w/o short contacts": "handled_w_o_short_contacts", 
                "Handled vs Compl goal": "vendor_handled_vs_compliance_goal",
                "Vendor Handled%": "digital_vendor_handled_pct",
                "AHT": "aht_sec",
            },
            "validate_float_columns": [
                "original_locks", "revised_locks",
                "handled", "handled_w_o_short_contacts",
                "vendor_handled_vs_compliance_goal", "digital_vendor_handled_pct"
                # "aht_sec", #"digital_hc_pct", 
            ],
        },
        "info_transform_function_affter":{
            "date_columns": [],
        },
        "save_information":{
            "keys": ["date", "call_type", "site"]
        }
    },
    "handled_compliance_inbound_geo":{
        "info_transform_function_before":{
            "int_columns": [],
            "float_columns": [],
            "date_columns": [],
        },
        "df_handling": {
            "order_columns": [
                "Week",
                "Intervals",
                "Passed Int",
                "SC%",
                "Time Interval",
                "Original Locks",
                "Revised Locks",
                "Compliance Goal",
                "Handled",
                "Handled w/o short contacts",
                "Handled vs Compl goal",
                "Vendor Handled%",
                "AHT"
            ],
            "rename_columns": {
                "Week":"week",
                "Intervals":"intervals",
                "Passed Int":"passed_int",
                "SC%":"sc_percent",
                "Time Interval": "date", 
                "Original Locks": "original_locks", 
                "Revised Locks": "revised_locks", 
                "Compliance Goal":"vendor_compliance_goal",
                "Handled": "handled",
                "Handled w/o short contacts": "handled_w_o_short_contacts", 
                "Handled vs Compl goal": "vendor_handled_vs_compliance_goal",
                "Vendor Handled%": "digital_vendor_handled_pct",
                "AHT": "aht_sec",
            },
            "validate_float_columns": [
                "original_locks", "revised_locks",
                "handled", "handled_w_o_short_contacts",
                "vendor_handled_vs_compliance_goal", "digital_vendor_handled_pct", 
                "week","intervals","passed_int","sc_percent" 
                # "aht_sec", #"digital_hc_pct", 
            ],
        },
        "info_transform_function_affter":{
            "date_columns": [],
        },
        "save_information":{
            "keys": ["date", "call_type", "site"]
        }
    }    
}