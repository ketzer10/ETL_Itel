# import packages
import src.tds.functions.global_tds_productivity_functions as tds_productivity_functions
import src.tds.functions.mbj_field_services_detailed_time_record_function as mbj_field_services_detailed_time_record_function
import numpy as np

configs = {
    "global_tds_sales_productivity": {
        "read_with_dtype": {
            "agent_id": object, 
            "agent_name": object, 
            "week_starting": object, 
            "quality_score": np.float64,
            "wrap_time": str, 
            "rgu_sales": np.float64, 
            "schedule_adherence": np.float64,	
            "supervisor": object,
            "operations_manager": object, 
            "location": object, 
            "site": object,
            "projection": object,
            "goal": object
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "agent_id", "agent_name", "week_starting", "quality_score",
                    "wrap_time", "rgu_sales", "schedule_adherence",	"supervisor",
                    "operations_manager", "location", "site", "projection", "goal"
                ],
                "replace_values_in_columns": [
                    {
                        "columns": ["wrap_time"],
                        "replace_this": ":00",
                        "for_this": ""
                    },
                    {
                        "columns": ["site"],
                        "replace_this": "MBJMC",
                        "for_this": "MBJ"
                    },
                    {
                        "columns": ["site"],
                        "replace_this": "SLUMC",
                        "for_this": "SLU"
                    }
                ],
                "validate_duration_columns": {
                    "columns": ["wrap_time"],
                    "parameters": {
                        "regex": "(^\d+\.?\d*):(\d+\.?\d*)"
                    }
                },
                "validate_text_columns": [
                    "agent_id", "agent_name", "supervisor",
                    "operations_manager", "location", "site"
                ],
                "validate_float_columns": [
                    "quality_score", "wrap_time", "rgu_sales", "schedule_adherence"
                ],
                "validate_int_columns": [
                    "projection", "goal"
                ],
                "validate_date_columns": {
                    "columns": ["week_starting"]
                },
                "rename_columns": {
                    "wrap_time": "wrap_time_sec"
                },
            },
        },
        "transform_function": tds_productivity_functions.transforms_function_sales_productivity,
        "delete_key": ["agent_id", "week_starting"],
    },
    "global_tds_repair_productivity":{
        "read_with_dtype": {
            "agent_id": object,
            "agent_name": str,
            "date": object,
            "quality_score": np.float64,
            "would_hire": np.float64,
            "average_handle": str,
            "repeat_tickets": np.float64,
            "escalated_tickets": np.float64,
            "supervisor": str,
            "operations_manager": str,
            "site": str,
            "location": str
        },
        "info_transform_function": {
            "df_handling": {
                "rename_columns": {
                    "average_handle":"average_handle_sec"
                },
                "validate_duration_columns": {
                    "columns": [
                        "average_handle_sec"
                    ],
                    "parameters": {
                        "regex": "(^\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)"
                    }
                },
                "validate_text_columns": [
                    "agent_name",
                    "supervisor",
                    "operations_manager",
                    "site",
                    "location"
                ],
                "validate_float_columns": [
                    "repeat_tickets",
                    "escalated_tickets",
                    "quality_score",
                    "would_hire"
                ],
                "validate_date_columns": {
                    "columns": ["date"]
                },
            }
        },
        "transform_function": tds_productivity_functions.transforms_function_repair_productivity
    },
    "global_tds_financial_services_productivity":{
        "read_with_dtype": {
            "agent_id": object,
            "agent_name": str,
            "week_start": str,
            "week_end": str,
            "adherence": "float64",
            "average_handle_out": str,
            "average_handle_in": str,
            "would_hire": "float64",
            "dollars_collected": "float64",
            "quality_audits": "float64",
            "dpa_audits": "float64",
            "processing_audits": "float64",
            "task_per_hour": "float64",
            "supervisor": str,
            "operations_manager": str,
            "location": str
        },
        "info_transform_function": {
            "df_handling": {
                "rename_columns": {
                    "average_handle_out":"average_handle_out_sec",
                    "average_handle_in":"average_handle_in_sec"
                },
                "validate_duration_columns": {
                    "columns": [
                        "average_handle_out_sec",
                        "average_handle_in_sec"
                    ],
                    "parameters": {
                        "regex": "(^\d+\.?\d*):(\d+\.?\d*)"
                    }
                },
                "validate_float_columns": [
                    "adherence",
                    "would_hire",
                    "dollars_collected",
                    "quality_audits",
                    "dpa_audits",
                    "processing_audits",
                    "task_per_hour"
                ],
                # "validate_date_columns": {
                #       "columns": ["week_end"]
                # },
                "validate_text_columns": [
                    "agent_id",
                    "agent_name",
                    "supervisor",
                    "operations_manager",
                    "location"
                ],
            }
        },
        "transform_function": tds_productivity_functions.transforms_function_financial_services_productivity
    },
    "global_tds_fields_services_productivity":{
        "read_with_dtype": {
            "agent_id": object,
            "agent_name": str,
            "date": object,
            "quality_score": object,
            "adherence": object,
            "average_handle": str,
            "tlt_error": np.float64,
            "error_rate": object,
            "inbound_calls": object,
            "supervisor": str,
            "operations_manager": str
        },
        "info_transform_function": {
            "df_handling": {
                "rename_columns": {
                    "average_handle":"average_handle_sec"
                },
                "validate_duration_columns": {
                    "columns": [
                        "average_handle_sec"
                    ],
                    "parameters":{
                        "regex":"(^\d+\.?\d*):(\d+\.?\d*)"
                    }
                },
                "validate_date_columns": {
                    "columns": ["date"]
                },
                "validate_float_columns": [
                    "adherence",
                    "quality_score",
                    "tlt_error"
                ],
                "validate_int_columns": [
                    "inbound_calls",
                    "error_rate"
                ],
                "validate_text_columns": [
                    "agent_id",
                    "agent_name",
                    "supervisor",
                    "operations_manager"
                ]
            }
        },
        "transform_function": tds_productivity_functions.transforms_function_fields_services_productivity   
    },
    "tds_detailed_time_record":{
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "Employee ID",
                    "Activity",
                    "Start",
                    "End",
                    "Paid Time (Hours)",
                    "Unpaid Time (Hours)",
                    "Total Time (Hours)",
                ],
                "rename_columns": {
                    "Paid Time (Hours)": "paid_time_hours",
                    "Unpaid Time (Hours)": "unpaid_time_hours",
                    "Total Time (Hours)": "total_time_hours",
                    "Start": "start",
                    "End": "end_",
                    "Activity": "activity",
                    "Employee ID": "employee_id"
                },
                "validate_float_columns": [
                    "paid_time_hours",
                    "unpaid_time_hours",
                    "total_time_hours"
                ],
                "validate_date_columns": {
                    "columns": [
                        "start",
                        "end_"
                    ],
                    "parameters": {
                        "date_format": "%Y-%m-%d %H:%M:%S"
                    }
                },
                "validate_text_columns": [
                    "activity",
                    "employee_id"
                ]
            }
        },
        "transform_function": mbj_field_services_detailed_time_record_function.tds_detailed_time_record_function
    }
    
}

























