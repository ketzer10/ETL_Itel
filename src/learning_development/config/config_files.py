# import packages
import src.learning_development.functions.glb_cx_daily_scores_functions as transforms_function

configs = {
    "global_training_calendar":{
        "info_transform_function_before":{
            "int_columns": [
                'YEAR', 'FTE', 'CS SCHEDULED AMOUNT', 'CS SHOWED AMOUNT', 'PRODUCT SCHEDULED AMOUNT', 'PRODUCT SHOWED AMOUNT',
                'GRADUATED', 'ATTRITION', 'SLATED TO START OJT', 'OJT GRADUATED', 'OJT ATTRITION', 'ROOM CAPACITY'
            ],
            "float_columns": [
                'TEST SCORES', 'CS + PRODUCT ATTENDANCE %', 'TEST SCORES', 
                'PRODUCT TRAINING BILLABLE HOURS', 'TSAT SCORE', 'GRADUATION %'
            ],
            "date_columns": [
                'START DATE', 'CUSTOMER SERVICE', 'CLIENT TRAINING',
                'END DATE', 'OJT START DATE', 'POST TRAINING FOLLOW-UP'
            ],
        },
        "df_handling": {
            "order_columns": [
                'YEAR', 'PERIOD', 'STATUS', 'ACCOUNT', 'BATCH #', 'TIME', 'TRAINER',
                'FTE', 'START DATE', 'CUSTOMER SERVICE', 'CLIENT TRAINING', 'END DATE',
                'OJT START DATE', 'POST TRAINING FOLLOW-UP', #'POST TRAINING STATUS',
                'TRAINING LOCATION', 'SITE', 'CS + PRODUCT ATTENDANCE %', 'TEST SCORES',
                'PRODUCT TRAINING BILLABLE HOURS', 'TSAT SCORE', 'CS SCHEDULED AMOUNT',
                'CS SHOWED AMOUNT', 'PRODUCT SCHEDULED AMOUNT', 'PRODUCT SHOWED AMOUNT',
                'GRADUATED', 'GRADUATION %', 'ATTRITION', 'SLATED TO START OJT',
                'OJT GRADUATED', 'OJT ATTRITION', 'ROOM CAPACITY'#,'POST TRAINING STATUS'
            ],
            "rename_columns": {
                'YEAR': 'year', 'PERIOD': 'period', 'STATUS': 'status', 'ACCOUNT': 'account', 
                'BATCH #': 'batch', 'TIME': 'time', 'TRAINER': 'trainer', 'FTE': 'fte', 
                'START DATE': 'start_date', 'CUSTOMER SERVICE': 'customer_service_date', 
                'CLIENT TRAINING': 'client_training_date', 'END DATE': 'end_date_date',
                'OJT START DATE': 'ojt_start_date', 'POST TRAINING FOLLOW-UP': 'post_training_follow_up_date', 
                #'POST TRAINING STATUS': 'post_training_status', 
                'TRAINING LOCATION': 'training_location', 
                'SITE': 'site', 'CS + PRODUCT ATTENDANCE %': 'cs_plus_product_attendance_pct', 
                'TEST SCORES': 'test_scores_pct', 'PRODUCT TRAINING BILLABLE HOURS': 'product_training_billable_hours', 
                'TSAT SCORE': 'tsat_score', 'CS SCHEDULED AMOUNT': 'cs_scheduled_amount',
                'CS SHOWED AMOUNT': 'cs_showed_amount', 'PRODUCT SCHEDULED AMOUNT': 'product_scheduled_amount', 
                'PRODUCT SHOWED AMOUNT': 'product_showed_amount', 'GRADUATED': 'graduated', 
                'GRADUATION %': 'graduation_pct', 'ATTRITION': 'attrition', 'SLATED TO START OJT': 'slated_to_start_ojt',
                'OJT GRADUATED': 'ojt_graduated', 'OJT ATTRITION': 'ojt_attrition', 'ROOM CAPACITY': 'room_capacity'
            },
            "validate_int_columns": [
                'year', 'fte', 'cs_scheduled_amount', 'cs_showed_amount', 'product_scheduled_amount',
                'product_showed_amount', 'graduated', 'attrition', 'slated_to_start_ojt', 'ojt_graduated', 'ojt_attrition', 'room_capacity'
            ],
            "validate_text_columns": [
                'period', 'status', 'account', 'batch', 'time', 'trainer', #'post_training_status', 
                'training_location', 'site', 
            ],
            "validate_float_columns": [
                'cs_plus_product_attendance_pct', 'test_scores_pct', 'product_training_billable_hours',
                'tsat_score', 'graduation_pct'
            ]
        },
        "info_transform_function_affter":{
            "date_columns": [
                'start_date', 'customer_service_date', 'client_training_date', 
                'end_date_date', 'ojt_start_date', 'post_training_follow_up_date'
            ],
        },
    },
    "glb_cx_daily_scores":{
        
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "Location",
                    "SVP",
                    "Manager",
                    "Business Unit",
                    "Metrics",
                    "Date",
                    "value"
                ],
                "rename_columns": {
                    "value": "value",
                    "Date": "date",
                    "Location": "location",
                    "SVP": "svp",
                    "Manager": "manager",
                    "Business Unit": "business_unit",
                    "Metrics": "metrics"
                },
                "validate_float_columns": [
                    "value"
                ],
                # "validate_date_columns": {
                #     "columns": [
                #         "date"
                #     ],
                #     "parameters": {
                #         "date_format": "%m/%d/%Y"
                #     }
                # },
                "validate_text_columns": [
                    "location",
                    "svp",
                    "manager",
                    "business_unit",
                    "metrics"
                ]
            }
        },
        "transform_function": transforms_function.transforms_function_glb_cx_daily_scores
    },
    "glb_cx_daily_reports_mtd":{
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "Location",
                    "SVP",
                    "Manager",
                    "Business Unit",
                    "Metrics",
                    "Month",
                    "Year",
                    "MTD"
                ],
                "rename_columns": {
                    "Location": "location",
                    "SVP": "svp",
                    "Manager": "manager",
                    "Business Unit": "business_unit",
                    "Metrics": "metrics",
                    "Month": "month",
                    "Year": "year",
                    "MTD": "mtd"

                },
                "validate_float_columns": [
                    "mtd"
                ],
                "validate_text_columns": [
                    "location",
                    "svp",
                    "manager",
                    "business_unit",
                    "metrics",
                    "month",
                    "year"
                ]
            }
        },
        "transform_function": transforms_function.transforms_function_glb_cx_daily_scores_mtd
    }
}