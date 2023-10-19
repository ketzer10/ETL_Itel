# import packages
import src.altice.functions.glb_altice_wfm_functions as transform_function
import src.altice.functions.glb_altice_commits_accepts_functions as transform_function_commits_accepts
from utils.dfutils import validate_text_columns

configs = {
    "glb_altice_wfm": {
        "read_with_dtype": {
            "required_fte": "int64",
            "scheduled_fte": "int64",
            "date": "datetime64",
            "interval": "str",
            "department":"str",
            "estimated_shrinkage_and_leakage":"float64"
        },
        "info_transform_function": {
            "df_handling": {
                "validate_int_columns": [
                    "required_fte",
                    "scheduled_fte"
                ],
                "validate_date_columns": {
                    "columns": [
                        "date"
                    ],
                    "parameters": {
                        "date_format": "%Y/%m/%d"
                    }
                },
                "validate_datetime_columns": {
                    "columns": [
                        "interval"
                    ],
                    "parameters": {
                        "date_format": "%H:%M:%S"
                    }
                },
                "validate_float_columns":["estimated_shrinkage_and_leakage"]
            }
    
        },
        "transform_function": transform_function.transforms_function_wfm_mbj_west
    },
    "glb_altice_commits_accepts":{
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "half_hour_interval",
                    "lob",
                    "committed_hours"
                ],
                "validate_float_columns": [
                    "committed_hours"
                ],
                "validate_datetime_columns": {
                    "columns": [
                        "half_hour_interval"
                    ],
                    "parameters": {
                        "date_format": "%Y-%m-%d %H:%M:%S"
                    }
                },
                "validate_text_columns": [
                    "lob"
                ]
            }
        },
        "transform_function": transform_function_commits_accepts.transforms_function_commits_accepts
    }
}