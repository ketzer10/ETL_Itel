import src.mia.functions.mia_csat_results_functions as transform_function 

configs = {
    "mia_csat_results": {
        "info_transform_function": {
            "df_handling": {                
                "order_columns": [
                    "date",
                    "dnis",
                    "ani",
                    "full_name",
                    "sklname",
                    "question1",
                    "question2",
                    "question3"
                ],

                "validate_date_columns": {
                    "columns": [
                        "date"
                    ],
                    "parameters": {
                        "date_format": "%m/%d/%Y %I:%M:%S %p"
                    }
                },
                "validate_int_columns": [
                    "dnis",
                    "ani",
                    "question1",
                    "question2",
                    "question3"

                ],
                "validate_text_columns": [
                    "full_name",
                    "sklname"
                ]
            }
        },
        "transform_function": transform_function.transforms_csat_results
    }
     
}