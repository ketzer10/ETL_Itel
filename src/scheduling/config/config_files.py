# import packages
import src.scheduling.functions.schedules_functions as transforms_function
import src.scheduling.functions.tds_hrm_employee_id_functions as tds_hrm_employee_id_functions
configs = {
    "slu_hilton_schedules":{
        "read_with_dtype": {
            "Nominal Date": "datetime64",
            "HRM_ID": "str",
            "Start": "str",
            "Stop": "str",
            "Code": "str"
        },
        "info_transform_function": {
            "code_remap_start":{
                "UBRK":"LunchStart", 
                "UBRK1":"Break 1 Start",
                "UBRK 2":"Break 2 Start", 
                "SHIFT":"TimeIn"
            },
            "code_remap_end":{
                "UBRK":"LunchEnd", 
                "UBRK1":"Break 1 End",
                "UBRK 2":"Break 2 End", 
                "SHIFT":"TimeOut"
            },
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start", "Break 2 End"],
            "df_handling": {
                "rename_columns": {
                    "Nominal Date": "date",
                    "HRM_ID": "Employee ID",
                    "Start": "Start",
                    "Stop": "Stop"
                },
                "strip_string_columns": ["Start","Stop"],
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%Y-%m-%d %H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_slu_hilton_schedules
    },
    "slu_altice_schedules":{
        "read_with_dtype": {
            "Nominal Date": object,
            "HRM": "str",
            "Start": "str",
            "Stop": "str",
            "Code": "str"
        },
        "info_transform_function": {
            "code_remap_start":{
                "UBRK1":"LunchStart", 
                "UBRK2-Lunch":"LunchStart", 
                "UBRK2-Lunch-OT":"LunchStart", 
                "UBRK3":"LunchStart",
                "PBRK1-1st-Break":"Break 1 Start",
                "PBRK3-2nd-Break":"Break 2 Start", 
                #"PBRK1-1st-Break-OT": "Break 3 Start",
                "SHIFT":"TimeIn"
            },
            "code_remap_end":{
                "UBRK1":"LunchEnd", 
                "UBRK2-Lunch":"LunchEnd", 
                "UBRK2-Lunch-OT":"LunchEnd", 
                "UBRK3":"LunchEnd",
                "PBRK1-1st-Break":"Break 1 End",        
                "PBRK3-2nd-Break":"Break 2 End", 
                #"PBRK1-1st-Break-OT": "Break 3 End",
                "SHIFT":"TimeOut"
            },
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End",
                              "Break 2 Start", "Break 2 End"],
            "df_handling": {
                "rename_columns": {
                    "Nominal Date": "date",
                    "HRM": "Employee ID"
                },
                "strip_string_columns": ["Start","Stop"],
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%I:%M %p"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_slu_altice_schedules
    },
    "slu_kroger_schedules":{
        "read_with_dtype": {
            "date": "str",
            "Employee ID": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str",
            "Break 3 Start": "str",
            "Break 3 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start","Break 3 End"],
                    "parameters":{
                        "date_format":"%H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        #"date_format":"%d-%m-%Y"
                        "date_format":"%m/%d/%Y"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_slu_kroger_schedules
    },
    "slu_tds_financial_services_schedules":{
        "read_with_dtype": {

        },
        "info_transform_function": {
            "code_remap_start":{
                "Break 1":"Break 1 Start", 
                "Break 2":"Break 2 Start", 
                "Lunch":"LunchStart", 
                "SHIFT":"TimeIn"
            },
            "code_remap_end":{
                "Break 1":"Break 1 End", 
                "Break 2":"Break 2 End", 
                "Lunch":"LunchEnd", 
                "SHIFT":"TimeOut"
            },
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "rename_columns": {
                    "Activity": "Code",
                    "End":"Stop"
                },
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%Y-%m-%d %H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_tds
    },
    "slu_tds_repairs_schedules":{
        "read_with_dtype": {

        },
        "info_transform_function": {
            "code_remap_start":{
                "Break 1":"Break 1 Start", 
                "Break 2":"Break 2 Start", 
                "Lunch":"LunchStart", 
                "SHIFT":"TimeIn"
            },
            "code_remap_end":{
                "Break 1":"Break 1 End", 
                "Break 2":"Break 2 End", 
                "Lunch":"LunchEnd", 
                "SHIFT":"TimeOut"
            },
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "rename_columns": {
                    "Activity": "Code",
                    "End":"Stop"
                },
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%Y-%m-%d %H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_tds
    },
    "slu_tds_sales_schedules":{
        "read_with_dtype": {

        },
        "info_transform_function": {
            "code_remap_start":{
                "Break 1":"Break 1 Start", 
                "Break 2":"Break 2 Start", 
                "Lunch":"LunchStart", 
                "SHIFT":"TimeIn"
            },
            "code_remap_end":{
                "Break 1":"Break 1 End", 
                "Break 2":"Break 2 End", 
                "Lunch":"LunchEnd", 
                "SHIFT":"TimeOut"
            },
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "rename_columns": {
                    "Activity": "Code",
                    "End":"Stop"
                },
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%Y-%m-%d %H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_tds
    },
    "mbj_tds_field_services_schedules":{
        "read_with_dtype": {

        },
        "info_transform_function": {
            "code_remap_start":{
                "Break 1":"Break 1 Start", 
                "Break 2":"Break 2 Start", 
                "Lunch":"LunchStart", 
                "SHIFT":"TimeIn"
            },
            "code_remap_end":{
                "Break 1":"Break 1 End", 
                "Break 2":"Break 2 End", 
                "Lunch":"LunchEnd", 
                "SHIFT":"TimeOut"
            },
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "rename_columns": {
                    "Activity": "Code",
                    "End":"Stop"
                },
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%Y-%m-%d %H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_tds
    },    
    "kgn_ancestry_schedules":{
        "read_with_dtype": {
            "Employee ID":"int64",
            "date":"datetime64",
            "Start":"str",
            "Stop":"str"
        },
        "info_transform_function": {

            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End","Break 3 Start","Break 3 End","Break 4 Start","Break 4 End"],
            "df_handling": {
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%d/%m/%y"
                    }
                },
                "validate_int_columns":["Employee ID"]
                
            },
        },
        "transform_function": transforms_function.transforms_function_kgn_ancestry_schedules
    },
    "tds_hrm_employee_id":{
        "read_with_dtype": {
            "HRM ID":"str",
            "HRM Name":"str",
            "TDS Name":"str",
            "TDS ID":"str",
            "Site":"str"
        },
        "info_transform_function": {
            
            "df_handling": {
                "rename_columns": {
                    "HRM ID": "hrm_id",
                    "HRM Name":"hrm_name",
                    "TDS Name":"tds_name",
                    "TDS ID":"tds_id",
                    "Site":"site",
                    "level_0":"department"
                },
                "replace_values_in_columns":[
                    {
                        "columns":["tds_id"],
                        "replace_this":"ID: ",
                        "for_this":""
                    }
                ],
                "validate_int_columns":["hrm_id","tds_id"],
                "validate_text_columns":["hrm_name","tds_name","site","department"]
            },
        },
        "transform_function": tds_hrm_employee_id_functions.transforms_function_tds_hrm_employee_id
    },
    "mbj_1800_flowers_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee Id": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str",
            "Break 3 Start": "str",
            "Break 3 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start","Break 3 End"],
                    "parameters":{
                        "date_format":"%m/%d/%Y %H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_mbj_1800_flowers
    },
    "slu_speedy_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee Id": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str",
            "Break 3 Start": "str",
            "Break 3 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start","Break 3 End"],
                    "parameters":{
                        "date_format":"%m/%d/%Y %H:%M"
                        #"date_format":"%Y-%m-%d %H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                        #"date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_slu_speedy
    },
    "mbj_speedy_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee Id": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str",
            "Break 3 Start": "str",
            "Break 3 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start","Break 3 End"],
                    "parameters":{
                        "date_format":"%m/%d/%Y %H:%M"
                        #"date_format":"%Y-%m-%d %H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                        #"date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_mbj_speedy
    },
    "mbj_activengage_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee_ID": "str",
            "Time_In": "str",
            "Time_Out": "str",
            "Lunch_Start": "str",
            "Lunch_End": "str",
            "Break_1_Start": "str",
            "Break_1_End": "str",
            "Break_2_Start": "str",
            "Break_2_End": "str",
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                    "parameters":{
                        "date_format":"%H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_mbj_activengage
    },
    "mbj_psn_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee Id": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                    "parameters":{
                        "date_format":"%H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_mbj_psn
    },
    "kgn_iaa_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee Id": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str",
            "Break 3 Start": "str",
            "Break 3 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start","Break 3 End"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y %H:%M"
                        "date_format":"%Y-%m-%d %H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y"
                        "date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_kgn_iaa
    },
    "mbj_ontellus_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee Id": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str",
            "Break 3 Start": "str",
            "Break 3 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start","Break 3 End"],
                    "parameters":{
                        "date_format":"%m/%d/%Y %H:%M"
                        #"date_format":"%Y-%m-%d %H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                        #"date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_mbj_ontellus
    },
    "mbj_moh_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee Id": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y %H:%M"
                        "date_format":"%H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y"
                        "date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_mbj_moh
    },
    "mbj_breville_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee_ID": "str",
            "Time_In": "str",
            "Time_Out": "str",
            "Lunch_Start": "str",
            "Lunch_End": "str",
            "Break_1_Start": "str",
            "Break_1_End": "str",
            "Break_2_Start": "str",
            "Break_2_End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y %H:%M"
                        "date_format":"%H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y"
                        "date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_mbj_breville
    },
    "mbj_car8_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee Id": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y %H:%M"
                        "date_format":"%H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y"
                        "date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_mbj_car8
    },
    "mbj_jps_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee Id": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str",
            "Break 3 Start": "str",
            "Break 3 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start","Break 3 End"],
                    "parameters":{
                        "date_format":"%m/%d/%Y %H:%M"
                        #"date_format":"%Y-%m-%d %H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                        #"date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_mbj_jps
    },
    "kgn_jps_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee Id": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str",
            "Break 3 Start": "str",
            "Break 3 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start","Break 3 End"],
                    "parameters":{
                        "date_format":"%m/%d/%Y %H:%M"
                        #"date_format":"%Y-%m-%d %H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                        #"date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_kgn_jps
    },
    "kgn_kroger_schedules":{
        "read_with_dtype": {
            "date": "str",
            "Employee ID": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str",
            "Break 3 Start": "str",
            "Break 3 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start","Break 3 End"],
                    "parameters":{
                        "date_format":"%H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        #"date_format":"%d-%m-%Y"
                        "date_format":"%m/%d/%Y"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_kgn_kroger_schedules
    }, 
    "kgn_hilton_schedules":{
        "read_with_dtype": {
            "Nominal Date": "datetime64",
            "HRM_ID": "str",
            "Start": "str",
            "Stop": "str",
            "Code": "str",
            "Site": "str"
        },
        "info_transform_function": {
            "code_remap_start":{
                "UBRK":"LunchStart", 
                "UBRK1":"Break 1 Start",
                "UBRK 2":"Break 2 Start", 
                "SHIFT":"TimeIn"
            },
            "code_remap_end":{
                "UBRK":"LunchEnd", 
                "UBRK1":"Break 1 End",
                "UBRK 2":"Break 2 End", 
                "SHIFT":"TimeOut"
            },
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start", "Break 2 End"],
            "df_handling": {
                "rename_columns": {
                    "Nominal Date": "date",
                    "HRM_ID": "Employee ID",
                    "Start": "Start",
                    "Stop": "Stop"
                },
                "strip_string_columns": ["Start","Stop"],
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%Y-%m-%d %H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_kgn_hilton_schedules
    }, 
    "mbj_hilton_schedules":{
        "read_with_dtype": {
            "Nominal Date": "datetime64",
            "HRM_ID": "str",
            "Start": "str",
            "Stop": "str",
            "Code": "str",
            "Site": "str"
        },
        "info_transform_function": {
            "code_remap_start":{
                "UBRK":"LunchStart", 
                "UBRK1":"Break 1 Start",
                "UBRK 2":"Break 2 Start", 
                "SHIFT":"TimeIn"
            },
            "code_remap_end":{
                "UBRK":"LunchEnd", 
                "UBRK1":"Break 1 End",
                "UBRK 2":"Break 2 End", 
                "SHIFT":"TimeOut"
            },
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start", "Break 2 End"],
            "df_handling": {
                "rename_columns": {
                    "Nominal Date": "date",
                    "HRM_ID": "Employee ID",
                    "Start": "Start",
                    "Stop": "Stop"
                },
                "strip_string_columns": ["Start","Stop"],
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%Y-%m-%d %H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_mbj_hilton_schedules
    },
    "kgn_tgcs_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee Id": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str",
            "Break 3 Start": "str",
            "Break 3 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start","Break 3 End"],
                    "parameters":{
                        "date_format":"%m/%d/%Y %H:%M"
                        #"date_format":"%Y-%m-%d %H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                        #"date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_kgn_jps
    },
    "mbj_tds_financial_services_schedules":{
        "read_with_dtype": {

        },
        "info_transform_function": {
            "code_remap_start":{
                "Break 1":"Break 1 Start", 
                "Break 2":"Break 2 Start", 
                "Lunch":"LunchStart", 
                "SHIFT":"TimeIn"
            },
            "code_remap_end":{
                "Break 1":"Break 1 End", 
                "Break 2":"Break 2 End", 
                "Lunch":"LunchEnd", 
                "SHIFT":"TimeOut"
            },
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "rename_columns": {
                    "Activity": "Code",
                    "End":"Stop"
                },
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%Y-%m-%d %H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_tds
    },      
    "mbj_tds_repairs_schedules":{
        "read_with_dtype": {

        },
        "info_transform_function": {
            "code_remap_start":{
                "Break 1":"Break 1 Start", 
                "Break 2":"Break 2 Start", 
                "Lunch":"LunchStart", 
                "SHIFT":"TimeIn"
            },
            "code_remap_end":{
                "Break 1":"Break 1 End", 
                "Break 2":"Break 2 End", 
                "Lunch":"LunchEnd", 
                "SHIFT":"TimeOut"
            },
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "rename_columns": {
                    "Activity": "Code",
                    "End":"Stop"
                },
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%Y-%m-%d %H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_tds
    },   
    "mbj_tds_sales_schedules":{
        "read_with_dtype": {

        },
        "info_transform_function": {
            "code_remap_start":{
                "Break 1":"Break 1 Start", 
                "Break 2":"Break 2 Start", 
                "Lunch":"LunchStart", 
                "SHIFT":"TimeIn"
            },
            "code_remap_end":{
                "Break 1":"Break 1 End", 
                "Break 2":"Break 2 End", 
                "Lunch":"LunchEnd", 
                "SHIFT":"TimeOut"
            },
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "rename_columns": {
                    "Activity": "Code",
                    "End":"Stop"
                },
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%Y-%m-%d %H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_tds
    },
    "kgn_mia_aesthetics_schedules":{
        "read_with_dtype": {
            "HRM ID ": "str",
            "HRM  ID ": "str",
            "Date ": "str",
            "Name": "str",
            "Start Time ": "str",
            "End Time ": "str",
            "Break 1 Start ": "str",
            "Break 1 End ": "str",
            "Lunch Start ": "str",
            "Lunch End ": "str",
            "Break 2 Start ": "str",
            "Break 2 End ": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y %H:%M"
                        #"date_format":"%Y-%m-%d %H:%M"
                        "date_format" : "%H:%M:%S"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y"
                        "date_format":"%Y-%m-%d %H:%M:%S"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_kgn_mia_aesthetics
    },
    "kgn_1800_flowers_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee Id": "str",
            "TimeIn": "str",
            "TimeOut": "str",
            "LunchStart": "str",
            "LunchEnd": "str",
            "Break 1 Start": "str",
            "Break 1 End": "str",
            "Break 2 Start": "str",
            "Break 2 End": "str",
            "Break 3 Start": "str",
            "Break 3 End": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start", "Break 3 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End","Break 3 Start","Break 3 End"],
                    "parameters":{
                        "date_format":"%m/%d/%Y %H:%M"
                        #"date_format":"%Y-%m-%d %H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                        #"date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_kgn_1800_flowers
    },
    "mbj_altice_schedules":{
        "read_with_dtype": {
            "Nominal Date": object,
            "HRM": "str",
            "Start": "str",
            "Stop": "str",
            "Code": "str"
        },
        "info_transform_function": {
            "code_remap_start":{
                "UBRK1":"LunchStart", 
                "UBRK2-Lunch":"LunchStart", 
                "UBRK2-Lunch-OT":"LunchStart", 
                "UBRK3":"LunchStart",
                "PBRK1-1st-Break":"Break 1 Start",
                "PBRK3-2nd-Break":"Break 2 Start", 
                #"PBRK1-1st-Break-OT": "Break 3 Start",
                "SHIFT":"TimeIn"
            },
            "code_remap_end":{
                "UBRK1":"LunchEnd", 
                "UBRK2-Lunch":"LunchEnd", 
                "UBRK2-Lunch-OT":"LunchEnd", 
                "UBRK3":"LunchEnd",
                "PBRK1-1st-Break":"Break 1 End",        
                "PBRK3-2nd-Break":"Break 2 End", 
                #"PBRK1-1st-Break-OT": "Break 3 End",
                "SHIFT":"TimeOut"
            },
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End",
                              "Break 2 Start", "Break 2 End"],
            "df_handling": {
                "rename_columns": {
                    "Nominal Date": "date",
                    "HRM": "Employee ID"
                },
                "strip_string_columns": ["Start","Stop"],
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%I:%M %p"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_slu_altice_schedules    
    },
    "kgn_altice_schedules":{
        "read_with_dtype": {
            "Nominal Date": object,
            "HRM": "str",
            "Start": "str",
            "Stop": "str",
            "Code": "str"
        },
        "info_transform_function": {
            "code_remap_start":{
                "UBRK1":"LunchStart", 
                "UBRK2-Lunch":"LunchStart", 
                "UBRK2-Lunch-OT":"LunchStart", 
                "UBRK3":"LunchStart",
                "PBRK1-1st-Break":"Break 1 Start",
                "PBRK3-2nd-Break":"Break 2 Start", 
                #"PBRK1-1st-Break-OT": "Break 3 Start",
                "SHIFT":"TimeIn"
            },
            "code_remap_end":{
                "UBRK1":"LunchEnd", 
                "UBRK2-Lunch":"LunchEnd", 
                "UBRK2-Lunch-OT":"LunchEnd", 
                "UBRK3":"LunchEnd",
                "PBRK1-1st-Break":"Break 1 End",        
                "PBRK3-2nd-Break":"Break 2 End", 
                #"PBRK1-1st-Break-OT": "Break 3 End",
                "SHIFT":"TimeOut"
            },
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End",
                              "Break 2 Start", "Break 2 End"],
            "df_handling": {
                "rename_columns": {
                    "Nominal Date": "date",
                    "HRM": "Employee ID"
                },
                "strip_string_columns": ["Start","Stop"],
                "validate_datetime_columns":{
                    "columns":["Start","Stop"],
                    "parameters":{
                        "date_format":"%I:%M %p"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%m/%d/%Y"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_slu_altice_schedules    
    },
    "kgn_lifetouch_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee ID": "str",
            "Time In": "str",
            "Time Out": "str",
            "LunchStart": "str",
            "lunch End": "str",
            "Break 1 Start": "str",
            "BreakStart": "str",
            "Break End": "str",
            "Break2 Start":"str",
            "Break 2 Start": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                    "parameters":{
                        "date_format":"%H:%M:%S"
                        #"date_format":"%Y-%m-%d %H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y"
                        #"date_format":"%Y-%m-%d"
                        "date_format":"%Y-%m-%d %H:%M"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_kgn_lifetouch
    },
    "kgn_shutterfly_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Employee ID": "str",
            "Time In": "str",
            "Time Out": "str",
            "LunchStart": "str",
            "Lunch End" : "str",
            "lunch End": "str",
            "Break 1 Start": "str",
            "BreakStart": "str",
            "Break End": "str",
            "Break 2 End": "str",
            "Break2 Start":"str",
            "Break 2 Start": "str"
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                    "parameters":{
                        "date_format":"%H:%M:%S"
                        #"date_format":"%Y-%m-%d %H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y"
                        #"date_format":"%Y-%m-%d"
                        "date_format":"%Y-%m-%d %H:%M"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_kgn_shutterfly
    },
    "mbj_liveperson_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Emp.ID": "str",
            "Start": "str",
            "End": "str",
            "Lunch Start": "str",
            "Lunch Stop": "str",
            "Break 1 Start": "str",
            "Break 1 Stop": "str",
            "Break 2 Start": "str",
            "Break 2 Stop": "str",
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y %H:%M"
                        "date_format":"%Y-%m-%d %H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%Y-%m-%d %H:%M"
                        #"date_format":"%m/%d/%Y"
                        #"date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_mbj_liveperson
    },
    "kgn_walmart_schedules":{
        "read_with_dtype": {
            "Date": "str",
            "Emp. ID": "str",
            "Start": "str",
            "End": "str",
            "Lunch Start": "str",
            "Lunch Stop": "str",
            "Break 1 Start": "str",
            "Break 1 Stop": "str",
            "Break 2 Start": "str",
            "Break 2 Stop": "str",
        },
        "info_transform_function": {
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End", "Break 2 Start","Break 2 End"],
            "df_handling": {
                "strip_string_columns": ["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                "validate_datetime_columns":{
                    "columns":["TimeIn","TimeOut","LunchStart","LunchEnd","Break 1 Start","Break 1 End","Break 2 Start","Break 2 End"],
                    "parameters":{
                        #"date_format":"%m/%d/%Y %H:%M"
                        "date_format":"%Y-%m-%d %H:%M"
                    }
                },
                "validate_date_columns":{
                    "columns":["date"],
                    "parameters":{
                        "date_format":"%Y-%m-%d %H:%M"
                        #"date_format":"%m/%d/%Y"
                        #"date_format":"%Y-%m-%d"
                    }
                }
                
            },
        },
        "transform_function": transforms_function.transforms_function_kgn_walmart
    }
}