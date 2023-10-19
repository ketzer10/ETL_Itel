# Share google sheet file with service account to be able to read them. Viewer access is fine. 
# import-data@itelautomations.iam.gserviceaccount.com

import utils.google_sheet_wrapper as gshw
import src.live_google_sheets.handling_functions_lib as lgsh_functions_lib

configs = {
    #===========================================================================================
    #===========================================================================================
    "files":{
        "Walmart Honduras Training Manual Tracker": {
            "information_file": {
                "file_id": "1nUhWsERX0rkl-aseGyMmd4AUQvQ2IoVYg4WkFB5c8UA",
                "file_url": "https://docs.google.com/spreadsheets/d/1nUhWsERX0rkl-aseGyMmd4AUQvQ2IoVYg4WkFB5c8UA/edit#gid=0"
            },
            "information_save_db": {
                "schema": "walmart",
                "table_name": "sap_training_hour_tracker"
            },
            "information_extract_worksheets": {
                "method": {
                    "ignore_worksheets": ["Directory", "Validation", "Hour Checker", "Hour Compiler"]
                },
                "head": 2
            }, 
            "handling_worksheets": gshw.handling_worksheets_add_source_tab_column,
            "expected_columns_for_stack": [
                "agent_name_id", "date", "schedule", "week_shift_type", "real_regular_start_time", 
                "real_regular_end_time", "lunch_hours", "ot_hours_am (5AM - 7PM)", 
                "ot_hours_mix (7PM - 10 PM)", "ot_hours_pm (10 PM - 5 AM)", 
                "regular_hours_worked", "is_valid", "agent_name", "legacy_id", 
                "schedule_start", "schedule_end", "scheduled_hours", "source_tab"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_honduras_manual_trackers,
            "grand_sheet_handling_todo": {
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_text_columns": [
                    "schedule", "week_shift_type", "agent_name", "legacy_id"
                ],
                "validate_datetime_columns": {
                    "columns":  [
                        "real_regular_start_time", "real_regular_end_time"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_hours", "ot_hours_am (5AM - 7PM)", "ot_hours_mix (7PM - 10 PM)", 
                        "ot_hours_pm (10 PM - 5 AM)", "regular_hours_worked", "scheduled_hours"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                
                "rename_columns": {
                    "lunch_hours": "lunch_sec",
                    "ot_hours_am (5AM - 7PM)": "ot_am_sec",
                    "ot_hours_mix (7PM - 10 PM)": "ot_mix_sec",
                    "ot_hours_pm (10 PM - 5 AM)": "ot_pm_sec",
                    "regular_hours_worked": "time_worked_sec",
                    "scheduled_hours": "scheduled_sec"
                },
                "strip_string_columns":{
                    "flag"
                },                
                "order_columns": [
                    "agent_name", "legacy_id", "date", "schedule",
                    "week_shift_type", "real_regular_start_time", 
                    "real_regular_end_time", "lunch_sec", "ot_am_sec",  
                    "ot_mix_sec", "ot_pm_sec", "time_worked_sec", "source_tab", 
                    "flag", "schedule_start", "schedule_end", "scheduled_sec"
                ]
            }
        },
        #===========================================================================================
        #===========================================================================================       
        "Walmart Honduras Operations Manual Tracker": {
            "information_file": {
                "file_id": "1cLSFpUgeqiSytsbwjnaoOAjgPixGA7WK4IuHEjCGU8A",
                "file_url": "https://docs.google.com/spreadsheets/d/1cLSFpUgeqiSytsbwjnaoOAjgPixGA7WK4IuHEjCGU8A/edit#gid=903515930",
            },
            "information_save_db": {
                "schema": "walmart",
                "table_name": "sap_operations_hour_tracker"
            },
            "information_extract_worksheets": {
                "method": {
                    "ignore_worksheets": ["Directory", "Validation"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.handling_worksheets_add_source_tab_column,
            "expected_columns_for_stack": [
                    "agent_name_id", "date", "schedule", "week_shift_type", "real_regular_start_time", 
                    "real_regular_end_time", "lunch_hours", "ot_hours_am (5AM - 7PM)", 
                    "ot_hours_mix (7:01 PM - 10 PM)", "ot_hours_pm (10:01 PM - 5 AM)", 
                    "regular_hours_worked", "is_valid", "agent_name", "legacy_id", 
                    "schedule_start", "schedule_end", "scheduled_hours", "source_tab"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_honduras_manual_trackers,
            "grand_sheet_handling_todo": {
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_text_columns": [
                    "schedule", "week_shift_type", "agent_name", "legacy_id"
                ],
                "validate_datetime_columns": {
                    "columns":  [
                        "real_regular_start_time", "real_regular_end_time"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_hours", "ot_hours_am (5AM - 7PM)", "ot_hours_mix (7:01 PM - 10 PM)", 
                        "ot_hours_pm (10:01 PM - 5 AM)", "regular_hours_worked", "scheduled_hours"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "rename_columns": {
                    "lunch_hours": "lunch_sec",
                    "ot_hours_am (5AM - 7PM)": "ot_am_sec",
                    "ot_hours_mix (7:01 PM - 10 PM)": "ot_mix_sec",
                    "ot_hours_pm (10:01 PM - 5 AM)": "ot_pm_sec",
                    "regular_hours_worked": "time_worked_sec",
                    "scheduled_hours": "scheduled_sec"
                },
                "strip_string_columns":{
                    "flag"
                },
                "order_columns": [
                    "agent_name", "legacy_id", "date", "schedule",
                    "week_shift_type", "real_regular_start_time", 
                    "real_regular_end_time", "lunch_sec", "ot_am_sec",  
                    "ot_mix_sec", "ot_pm_sec", "time_worked_sec", "source_tab", 
                    "flag", "schedule_start", "schedule_end", "scheduled_sec"
                ]
            }
        },
        #===========================================================================================
        #===========================================================================================
        "Anyone Home Honduras Operations Manual Tracker": {
            "information_file": {
                "file_id": "1TQYBwSZiKULtoeVsDghGGqx667p2kMO1qRorDUtFUHU",
                "file_url": "https://docs.google.com/spreadsheets/d/1TQYBwSZiKULtoeVsDghGGqx667p2kMO1qRorDUtFUHU/edit#gid=903515930"
            },
            "information_save_db": {
                "schema": "anyone_home",
                "table_name": "sap_operations_hour_tracker",
            },
            "information_extract_worksheets": {
                "method": {
                    "ignore_worksheets": ["Directory", "Validation"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.handling_worksheets_add_source_tab_column,
            "expected_columns_for_stack": [
                "agent_name_id", "date", "schedule", "week_shift_type", "real_regular_start_time", 
                "real_regular_end_time", "lunch_hours", "ot_hours_am (5AM - 7PM)", 
                "ot_hours_mix (7:01 PM - 10 PM)", "ot_hours_pm (10:01 PM - 5 AM)", 
                "regular_hours_worked", "is_valid", "agent_name", "legacy_id", 
                "schedule_start", "schedule_end", "scheduled_hours", "source_tab"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_honduras_manual_trackers,
            "grand_sheet_handling_todo": {
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_text_columns": [
                    "schedule", "week_shift_type", "agent_name", "legacy_id"
                ],
                "validate_datetime_columns": {
                    "columns":  [
                        "real_regular_start_time", "real_regular_end_time"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_hours", "ot_hours_am (5AM - 7PM)", "ot_hours_mix (7:01 PM - 10 PM)", 
                        "ot_hours_pm (10:01 PM - 5 AM)", "regular_hours_worked", "scheduled_hours"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "rename_columns": {
                    "lunch_hours": "lunch_sec",
                    "ot_hours_am (5AM - 7PM)": "ot_am_sec",
                    "ot_hours_mix (7:01 PM - 10 PM)": "ot_mix_sec",
                    "ot_hours_pm (10:01 PM - 5 AM)": "ot_pm_sec",
                    "regular_hours_worked": "time_worked_sec",
                    "scheduled_hours": "scheduled_sec"
                },
                "strip_string_columns":{
                    "flag"
                },                
                "order_columns": [
                    "agent_name", "legacy_id", "date", "schedule",
                    "week_shift_type", "real_regular_start_time", 
                    "real_regular_end_time", "lunch_sec", "ot_am_sec",  
                    "ot_mix_sec", "ot_pm_sec", "time_worked_sec", "source_tab", 
                    "flag", "schedule_start", "schedule_end", "scheduled_sec"
                ]
            }
        },
        #===========================================================================================
        #===========================================================================================
        "Anyone Home Honduras Training Manual Tracker": {
            "information_file": {
                "file_id": "1vbc_WMwxBWrJtmzIUhWGrr5m2nPxg9EX5obP--X9K5A",
                "file_url": "https://docs.google.com/spreadsheets/d/1vbc_WMwxBWrJtmzIUhWGrr5m2nPxg9EX5obP--X9K5A/edit#gid=903515930"
            },
            "information_save_db": {
                "schema": "anyone_home",
                "table_name": "sap_training_hour_tracker"
            },
            "information_extract_worksheets": {
                "method": {
                    "ignore_worksheets": ["Directory", "Validation"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.handling_worksheets_add_source_tab_column,
            "expected_columns_for_stack": [
                "agent_name_id", "date", "schedule", "week_shift_type", "real_regular_start_time", 
                "real_regular_end_time", "lunch_hours", "ot_hours_am (5AM - 7PM)", 
                "ot_hours_mix (7:01 PM - 10 PM)", "ot_hours_pm (10:01 PM - 5 AM)", 
                "regular_hours_worked", "is_valid", "agent_name", "legacy_id", 
                "schedule_start", "schedule_end", "scheduled_hours", "source_tab"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_honduras_manual_trackers,
            "grand_sheet_handling_todo": {
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_text_columns": [
                    "schedule", "week_shift_type", "agent_name", "legacy_id"
                ],
                "validate_datetime_columns": {
                    "columns":  [
                        "real_regular_start_time", "real_regular_end_time"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_hours", "ot_hours_am (5AM - 7PM)", "ot_hours_mix (7:01 PM - 10 PM)", 
                        "ot_hours_pm (10:01 PM - 5 AM)", "regular_hours_worked", "scheduled_hours"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "rename_columns": {
                    "lunch_hours": "lunch_sec",
                    "ot_hours_am (5AM - 7PM)": "ot_am_sec",
                    "ot_hours_mix (7:01 PM - 10 PM)": "ot_mix_sec",
                    "ot_hours_pm (10:01 PM - 5 AM)": "ot_pm_sec",
                    "regular_hours_worked": "time_worked_sec",
                    "scheduled_hours": "scheduled_sec"
                },
                "strip_string_columns":{
                    "flag"
                },                
                "order_columns": [
                    "agent_name", "legacy_id", "date", "schedule",
                    "week_shift_type", "real_regular_start_time", 
                    "real_regular_end_time", "lunch_sec", "ot_am_sec",  
                    "ot_mix_sec", "ot_pm_sec", "time_worked_sec", "source_tab", 
                    "flag", "schedule_start", "schedule_end", "scheduled_sec"
                ]
            }
        },
        #===========================================================================================
        #===========================================================================================
        "Honduras Medical Leaves": {
            "information_file": {
                "file_id": "1_Z8FAcHqtDtkN9-fbigljmOQ8H5UjCihNfo6tYVxhQI",
                "file_url": "https://docs.google.com/spreadsheets/d/1_Z8FAcHqtDtkN9-fbigljmOQ8H5UjCihNfo6tYVxhQI/edit#gid=1749359525",
            },
             "information_save_db": {
                "schema": "hr",
                "table_name": "sap_medical_leaves",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Leaves"]
                },
                "head": 1
            },
            "handling_worksheets": lgsh_functions_lib.handling_worksheets_sap_medical_leaves,
            "expected_columns_for_stack": [
                "medical_excuse_date", "agent_name_id", "supervisor_name_id", "client", "shift_type", 
                "hours", "comments", "incidence_type", "doctor_name", "diagnostic", 
                "specific_type", "name_clinic", "approved", "revision_date", "revised_by", "HR_Observation" ,
                "itel_coverage", 'agent_name', 'legacy_id', 'flag'
            ],
            "handling_grand_worksheet": gshw.pass_function_grand_worksheet,
            "grand_sheet_handling_todo": {
                "rename_columns":{
                    "shift_type": "week_shift_type", "medical_excuse_date":"date"
                },            
                "validate_date_columns": {
                    "columns":[
                        "date", "revision_date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_text_columns": [
                    "agent_name", "legacy_id", "client", "week_shift_type", "diagnostic", 
                    "incidence_type", "revised_by", "approved"
                ],
                "validate_float_columns": [
                    "hours", "itel_coverage"
                ],
                "order_columns": [
                    "date", "client", "week_shift_type", "hours", "diagnostic", 
                    "incidence_type", "approved", "revision_date", "revised_by", "agent_name", 
                    "legacy_id", "flag", "itel_coverage"
                ]
            }
        },
        #===========================================================================================
        #===========================================================================================                
        "Anyone Home Guyana Training Tracker": {
            "information_file": {
                "file_id": "1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw",
                "file_url": "https://docs.google.com/spreadsheets/d/1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw/edit#gid=1309853082",
            },
             "information_save_db": {
                "schema": "anyone_home",
                "table_name": "geo_manual_tracker_training",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Anyone Home"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },                
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },          
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },        
        #===========================================================================================
        #===========================================================================================       
        "Liveperson Guyana Training Tracker": {
            "information_file": {
                "file_id": "1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw",
                "file_url": "https://docs.google.com/spreadsheets/d/1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw/edit#gid=1077543555",
            },
             "information_save_db": {
                "schema": "liveperson",
                "table_name": "geo_manual_tracker_training",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Liveperson_Altice_Optimum"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },                
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },        
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },        
        #===========================================================================================
        #===========================================================================================  
        "Office Depot BPO Guyana Training Tracker": {
            "information_file": {
                "file_id": "1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw",
                "file_url": "https://docs.google.com/spreadsheets/d/1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw/edit#gid=996711426",
            },
             "information_save_db": {
                "schema": "office_depot",
                "table_name": "geo_manual_tracker_training",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Office_Depot_BPO"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },              
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                                
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },        
        #===========================================================================================
        #===========================================================================================              
        "Office Depot WAH Training Tracker": {
            "information_file": {
                "file_id": "1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw",
                "file_url": "https://docs.google.com/spreadsheets/d/1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw/edit#gid=1618029308",
            },
             "information_save_db": {
                "schema": "office_depot",
                "table_name": "wah_manual_tracker_training",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Office_Depot_WAH"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },              
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                 
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },        
        #===========================================================================================
        #===========================================================================================   
        "Maxsold Training Tracker": {
            "information_file": {
                "file_id": "1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw",
                "file_url": "https://docs.google.com/spreadsheets/d/1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw/edit#gid=1618029308",
            },
             "information_save_db": {
                "schema": "maxsold",
                "table_name": "geo_manual_tracker_training",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["MaxSold"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },              
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                 
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },        
        #===========================================================================================
        #===========================================================================================
        "ActivEngage Training Tracker": {
            "information_file": {
                "file_id": "1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw",
                "file_url": "https://docs.google.com/spreadsheets/d/1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw/edit#gid=1618029308",
            },
             "information_save_db": {
                "schema": "active_engage",
                "table_name": "geo_manual_tracker_training",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["ActivEngage"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },              
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                 
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },        
        #===========================================================================================
        #===========================================================================================
        "ActivEngage Operations Tracker": {
            "information_file": {
                "file_id": "1qWHTo76xSW1fOm3MwF-9Uzn33mW7jzVLu-cneRU-RoM",
                "file_url": "https://docs.google.com/spreadsheets/d/1qWHTo76xSW1fOm3MwF-9Uzn33mW7jzVLu-cneRU-RoM/edit#gid=0",
            },
             "information_save_db": {
                "schema": "active_engage",
                "table_name": "geo_manual_tracker_operations",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Hour_Tracker"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },              
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                 
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },        
        #===========================================================================================
        #===========================================================================================
        "Maxsold Operations Tracker": {
            "information_file": {
                "file_id": "1NStlRB92xqzWlTvCidGLr7gSzJdlyVqRKytSWzvYq6E",
                "file_url": "https://docs.google.com/spreadsheets/d/1NStlRB92xqzWlTvCidGLr7gSzJdlyVqRKytSWzvYq6E/edit#gid=996711426",
            },
             "information_save_db": {
                "schema": "maxsold",
                "table_name": "geo_manual_tracker_operations",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Hour_Tracker"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },              
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                 
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },        
        #===========================================================================================
        #===========================================================================================  
        "Office Depot Mappings": {
            "information_file": {
                "file_id": "1Qn-LYGgu4Y9x5TFvmVnyURiVbakccaLkJi-bAwhnr3o",
                "file_url": "https://docs.google.com/spreadsheets/d/1Qn-LYGgu4Y9x5TFvmVnyURiVbakccaLkJi-bAwhnr3o/edit?pli=1#gid=961522481",
            },
             "information_save_db": {
                "schema": "office_depot",
                "table_name": "glb_mappings",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Office Depot Roster"]
                },
                "head": 1
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "emerge_id", "hr_name", "team_time_id", "office_depot_id", "journey_id", "chat_username", "sms_username", 
                "on_hold_table_id", "office_depot_email", "supervisor", "line_business", "was_transferred", 
                "employee_title", "status"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_office_depot_mappings,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "emerge_id": "legacy_id",
                    "hr_name": "employee_name"
                },                           
                "validate_text_columns": [
                    "legacy_id", "employee_name", "team_time_id", "office_depot_id", "journey_id", "chat_username", 
                    "on_hold_table_id", "office_depot_email", "supervisor", "line_business", "was_transferred", 
                    "employee_title", "status"
                ],
                "strip_string_columns":[
                    "journey_id", "office_depot_id", "chat_username", "on_hold_table_id", "office_depot_email"
                ],                 
                "upper_string_columns":[
                    "journey_id" 
                ],                               
                "order_columns": [
                    "employee_name", "team_time_id", "office_depot_id", "legacy_id", "supervisor", "line_business", "employee_title", 
                    "status", "was_transferred", "chat_username", "journey_id", "office_depot_email", "on_hold_table_id", "sms_username"
                ]                
            }
        },        
        #===========================================================================================
        #===========================================================================================     
        "Liveperson Mappings": {
            "information_file": {
                "file_id": "1ycC2SccLABWJyua36AUxzWO4D7KjkzJprpoxO24zmWY",
                "file_url": "https://docs.google.com/spreadsheets/d/1ycC2SccLABWJyua36AUxzWO4D7KjkzJprpoxO24zmWY/edit#gid=961522481",
            },
             "information_save_db": {
                "schema": "liveperson",
                "table_name": "glb_mappings",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Liveperson Roster"]
                },
                "head": 1
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "emerge_id", "hr_name", "liveperson_id", "agent_email", "medallia_name", 
                "medallia_cc_rep_id", "peoplesoft_id", "altice_email", "network_id", "wave", "status", 
                "skill", "supervisor", "employee_title", "liveengage_altice_id", "liveengage_altice_email"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_liveperson_mappings,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "emerge_id": "legacy_id",
                    "hr_name": "employee_name",
                    "medallia_cc_rep_id": "medallia_id"
                },                           
                "validate_text_columns": [
                    "legacy_id", "employee_name", "liveperson_id", "agent_email", "medallia_name", 
                    "medallia_id", "peoplesoft_id", "altice_email", "network_id", "wave", "status", 
                    "skill", "supervisor", "employee_title", "liveengage_altice_id", "liveengage_altice_email"
                ],
                "order_columns": [
                    "employee_name", "liveperson_id", "agent_email", "status", "skill", "legacy_id", "medallia_id", 
                    "supervisor", "peoplesoft_id", "altice_email", "network_id", "medallia_name", "wave", "liveengage_altice_id", 
                    "liveengage_altice_email"
                ]               
            }
        },        
        #===========================================================================================
        #===========================================================================================      
        "Anyone Home Mappings": {
            "information_file": {
                "file_id": "1zycD9GMeMVWNo9oFR7dOL0p9oujzBeDHeSBN5czbkPo",
                "file_url": "https://docs.google.com/spreadsheets/d/1zycD9GMeMVWNo9oFR7dOL0p9oujzBeDHeSBN5czbkPo/edit#gid=961522481",
            },
             "information_save_db": {
                "schema": "anyone_home",
                "table_name": "glb_mappings",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Anyone Home Roster"]
                },
                "head": 1 
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "emerge_id", "hr_name", "agent_email", "aoh_id", "adherence_id", 
                "external_qa_name", "wave", "supervisor", "was_transferred",
                "employee_title", "status"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_anyonehome_mappings,
            "grand_sheet_handling_todo": {
                # fill_df_nulls is used to fill blanks with nulls before using upper() or lower() because they get converted to 
                # strings with Null like values that are actually strings.
                "fill_df_nulls": "", 
                "rename_columns": {
                    "aoh_id": "anyone_home_id",
                    "hr_name": "employee_name",
                    "agent_email": "anyone_home_email",
                    "emerge_id": "legacy_id"
                },
                "order_columns": [
                    "anyone_home_id", "employee_name", "anyone_home_email", "legacy_id", 
                    "supervisor", "adherence_id", "external_qa_name", "wave"
                ],            
                "upper_string_columns":[
                    "adherence_id", "anyone_home_email"
                ],
                "strip_string_columns":[
                    "adherence_id", "anyone_home_email"
                ],
                "validate_text_columns": [
                    "anyone_home_id", "employee_name", "anyone_home_email", "legacy_id", 
                    "supervisor", "adherence_id", "external_qa_name", "wave"
                ]                  
            }
        },
        #===========================================================================================
        #=========================================================================================== 
        "Office Depot BPO Exceptions": {
            "information_file": {
                "file_id": "1CncZw-QB8A8MUSo_-EuRdvxVQJX1Jo8O31ZitlF_FoE",
                "file_url": "https://docs.google.com/spreadsheets/d/1CncZw-QB8A8MUSo_-EuRdvxVQJX1Jo8O31ZitlF_FoE/edit#gid=1496789356",
            },
             "information_save_db": {
                "schema": "office_depot",
                "table_name": "geo_exceptions",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Form Responses 1"]
                },
                "head": 1 
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Timestamp", "Email Address", "Agent Name", "Date of exception", "Start time of exception", 
                "End time of exception", "Exception category", "Additional notes", "Duration", "agent_name", 
                "emerge_id", "is_valid", "approved", "approver", "isduplicate"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_worksheet_google_form_responses_timestamp,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "Timestamp": "timestamp",
                    "Email Address": "email_address",                    
                    "Date of exception": "exception_date",
                    "Start time of exception": "start_of_exception",
                    "End time of exception": "end_of_exception",
                    "Exception category": "exception_category",
                    "Additional notes": "additional_notes",
                    "Duration": "duration_seconds",
                    "emerge_id": "legacy_id",
                    "approved": "approval_status"                    
                },
                "order_columns": [
                    "timestamp", "email_address", "agent_name", "exception_category", "additional_notes", 
                    "duration_seconds", "legacy_id", "is_valid", "approval_status", "approver", "exception_date", 
                    "start_of_exception", "end_of_exception"
                ],
                "validate_date_columns": {
                    "columns":[
                        "exception_date"
                    ]
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_of_exception", "end_of_exception"
                    ]
                },                
                "validate_duration_columns": {
                    "columns":  [
                        "duration_seconds"
                    ]
                },                             
                "validate_text_columns": [
                    "email_address", "agent_name", "exception_category", "additional_notes",
                    "legacy_id", "is_valid", "approval_status", "approver"
                ]                  
            }
        },             
        #===========================================================================================
        #=========================================================================================== 
        "Liveperson Exceptions": {
            "information_file": {
                "file_id": "1EUcRrKfDqCOdcgCcX9p0ifAQEvyI4q9JVuTabhNPPyE",
                "file_url": "https://docs.google.com/spreadsheets/d/1EUcRrKfDqCOdcgCcX9p0ifAQEvyI4q9JVuTabhNPPyE/edit#gid=514131815",
            },
             "information_save_db": {
                "schema": "liveperson",
                "table_name": "geo_exceptions",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Merged Responses"]
                },
                "head": 1 
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Timestamp", "Email Address", "Client and line of business", "Agent name", "Agent Name", 
                "Date of exception", 
                "Start time of exception", "End time of exception", "Exception category", "Additional notes", 
                "Final_Agent", "Duration", "is_valid", "Approval_Status", "Approver", "Approver_Notes", "Is_Duplicate", 
                "Agent_Name", "Emerge_ID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_worksheet_google_form_responses_timestamp,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "Timestamp": "timestamp",
                    "Email Address": "email_address",                    
                    "Date of exception": "exception_date",
                    "Start time of exception": "start_of_exception",
                    "End time of exception": "end_of_exception",
                    "Exception category": "exception_category",                    
                    "Duration": "duration_sec",
                    "Agent_Name": "agent_name",
                    "Emerge_ID": "legacy_id",
                    "Final_Agent": "agent_name_id",
                    "Approver": "approver",
                    "Approval_Status": "approval_status"                    
                },
                "validate_date_columns": {
                    "columns":[
                        "exception_date"
                    ]
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_of_exception", "end_of_exception"
                    ]   
                },
                "validate_duration_columns":{
                    "columns":[
                        "duration_sec"
                    ]
                },         
                "validate_text_columns": [
                    "email_address", "agent_name", "exception_category", "agent_name_id",
                    "legacy_id", "is_valid", "approval_status", "approver"
                ],
                "order_columns": [
                    "timestamp", "email_address", "agent_name", "exception_date", "start_of_exception", 
                    "end_of_exception", "duration_sec", "legacy_id", "is_valid", "approval_status", 
                    "agent_name_id", "approver", "exception_category"
                ]                            
            }
        },
        #===========================================================================================
        #=========================================================================================== 
        "Anyone Home Exceptions": {
            "information_file": {
                "file_id": "1q2kKp2xGKKxgyzVQ2_BXEtkDNFVyW9TRyrZCJ1gyIdo",
                "file_url": "https://docs.google.com/spreadsheets/d/1q2kKp2xGKKxgyzVQ2_BXEtkDNFVyW9TRyrZCJ1gyIdo/edit#gid=250649947",
            },
             "information_save_db": {
                "schema": "anyone_home",
                "table_name": "geo_exceptions",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Form Responses 2"]
                },
                "head": 1 
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Timestamp", "Email Address", "Agent Name", "Date of exception", "Start time of exception", 
                "End time of exception", "Exception category", "Additional notes", "Duration", "agent_name", 
                "emerge_id", "is_valid", "approved", "approver", "isduplicate"
            ],
            "handling_grand_worksheet": gshw.pass_function_grand_worksheet,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "Timestamp": "timestamp",
                    "Email Address": "email_address",                    
                    "Date of exception": "exception_date",
                    "Start time of exception": "start_of_exception",
                    "End time of exception": "end_of_exception",
                    "Exception category": "exception_category",
                    "Additional notes": "additional_notes",
                    "Duration": "duration_seconds",
                    "emerge_id": "legacy_id",
                    "approved": "approval_status"                    
                },
                "order_columns": [
                    "timestamp", "email_address", "agent_name", "exception_category", "additional_notes", 
                    "duration_seconds", "legacy_id", "is_valid", "approval_status", "approver", "exception_date", 
                    "start_of_exception", "end_of_exception"
                ],
                "validate_date_columns": {
                    "columns":[
                        "exception_date"
                    ]
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_of_exception", "end_of_exception"
                    ]
                },
                "convert_to_datetime_columns":[
                    "timestamp"
                ],                
                "validate_duration_columns": {
                    "columns":  [
                        "duration_seconds"
                    ]
                },            
                "validate_text_columns": [
                    "email_address", "agent_name", "exception_category", "additional_notes",
                    "legacy_id", "is_valid", "approval_status", "approver"
                ]                  
            }
        },
        #===========================================================================================
        #===========================================================================================
        "Honduras Payroll Queries": {
            "information_file": {
                "file_id": "1I8-_Hdc6D-NzQOHMm6TMUXpD7RRMkAzwvPA9w10GYaM",
                "file_url": "https://docs.google.com/spreadsheets/d/1I8-_Hdc6D-NzQOHMm6TMUXpD7RRMkAzwvPA9w10GYaM/edit#gid=1639288429",
            },
             "information_save_db": {
                "schema": "hr",
                "table_name": "sap_payroll_queries",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Queries"]
                },
                "head": 1
            },
            "handling_worksheets": lgsh_functions_lib.handling_worksheets_sap_medical_leaves,
            "expected_columns_for_stack": [
                "agent_name_id", "paid_on", "total_usd", "comments", 'agent_name', 'legacy_id', 'flag'
            ],
            "handling_grand_worksheet": gshw.pass_function_grand_worksheet,
            "grand_sheet_handling_todo": {     
                "validate_date_columns": {
                    "columns":[
                        "paid_on"
                    ]
                },
                "validate_text_columns": [
                    "agent_name_id", "comments", 'agent_name', 'legacy_id', 'flag'
                ],
                "validate_float_columns": [
                    "total_usd"
                ],
                "validate_date_columns" :{
                    "columns" : ["paid_on"]
                },
                "order_columns": [
                    "agent_name", "legacy_id", "paid_on", "total_usd"
                ]
            }
        },
        #===========================================================================================
        #===========================================================================================
        "Honduras Bonuses": {
            "information_file": {
                "file_id": "1G3GUQOwYkBui3hcLQXEmB-wQa5qVNUXxsA_dkLttnMM",
                "file_url": "https://docs.google.com/spreadsheets/d/1G3GUQOwYkBui3hcLQXEmB-wQa5qVNUXxsA_dkLttnMM/edit#gid=352190823",
            },
             "information_save_db": {
                "schema": "hr",
                "table_name": "sap_bonuses",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Hiring Bonus"]
                },
                "head": 1
            },
            "handling_worksheets": lgsh_functions_lib.handling_worksheets_sap_medical_leaves,
            "expected_columns_for_stack": [
                "agent_name_id", "paid_on", "hiring_bonus_payout", "referral_bonus_payout", 
                "attendance_bonus_payout", 'agent_name', 'legacy_id', 'flag'
            ],
            "handling_grand_worksheet": gshw.pass_function_grand_worksheet,
            "grand_sheet_handling_todo": {   
                "validate_date_columns": {
                    "columns":[
                        "paid_on"
                    ]
                },
                "validate_text_columns": [
                    "agent_name", "legacy_id"
                ],
                "validate_float_columns": [
                    "hiring_bonus_payout", "referral_bonus_payout", "attendance_bonus_payout"
                ],
                "order_columns": [
                    "agent_name", "legacy_id", "paid_on", "hiring_bonus_payout", "referral_bonus_payout", 
                "attendance_bonus_payout"
                ]
            }
        },
        #===========================================================================================
        #===========================================================================================        
        "Hilton Training Tracker": {
            "information_file": {
                "file_id": "1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw",
                "file_url": "https://docs.google.com/spreadsheets/d/1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw/edit#gid=1618029308",
            },
             "information_save_db": {
                "schema": "hilton",
                "table_name": "geo_manual_tracker_training",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Hilton"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },              
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                 
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },        
        #===========================================================================================
        #===========================================================================================
        "Hilton Operations Tracker": {
            "information_file": {
                "file_id": "1moIlZbSXmvxSG3JHhsBuR4jzDYp3bPLI9Z-PsdVffaY",
                "file_url": "https://docs.google.com/spreadsheets/d/1moIlZbSXmvxSG3JHhsBuR4jzDYp3bPLI9Z-PsdVffaY/edit#gid=0",
            },
             "information_save_db": {
                "schema": "hilton",
                "table_name": "geo_manual_tracker_operations",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Hour_Tracker"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },              
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                 
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },
        #===========================================================================================
        #===========================================================================================
        "Office Depot QA 2022": {
            "information_file": {
                "file_id": "1Vk70wk4ubbxpzyzfYzcQBjNrGMgRbOPPtiuzfanVNVk",
                "file_url": "https://docs.google.com/spreadsheets/d/1Vk70wk4ubbxpzyzfYzcQBjNrGMgRbOPPtiuzfanVNVk",
            },
             "information_save_db": {
                "schema": "office_depot",
                "table_name": "geo_google_sheets_internal_qa",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Form Responses 1"]
                },
                "head": 1
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Timestamp", "Email Address", "Session ID", "QA Auditor", 
                "Acknowledge the caller/customer, matched style and pace/put Customer at ease?", 
                "CCP made the Customer feel important and top priority?", " Appropriate and sincere use of empathy?", 
                "Customer clearly understood the CCP, CCP used proper English? (no OD jargon)", 
                "CCP recognized Customer contacted us multiple times regarding the same issue and escalated to Supervisor/Team Lead as appropriate?", 
                "[Phone] CCP verified line item, quantity, price, total and delivery info AS NEEDED to place the order/return?", 
                "Followed SOP/iDepot article and account level pop up box instructions while maintaining control of the call/chat/sms?", 
                "CCP noted appropriately? (Transaction History, Special Instructions, etc.)", 
                "CCP listened/read/comprehended and paraphrased/understood the customer, identified wants/needs and gained agreement by asking open-ended follow up questions?", 
                "[Chat/SMS] CCP maintained control of the conversation/chat?", "CCP verified information as appropriate to the call/chat, proactively utilized CTI (phone), utilized the bot/pre-chat window (chat)?", 
                "Did the CCP submit the proper forms based on the resolution needed and summarize the resolutions steps?",
                 "Was the proper disposition code used?", "General comments", "Supervisor", "LOB", "Employee Name", "Score"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_office_depot_qa,
            "grand_sheet_handling_todo": {        
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                },                
                "validate_text_columns": [
                    "email_address", "session_id", "employee_id", "employee_name", "q1", "q2", 
                     "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "supervisor", 
                      "supervisor_id", "lob", "quality_auditor_id", "quality_auditor_name" 
                ], 
                "validate_float_columns":[
                    "score"
                ],
                "order_columns": [
                    "date", "email_address", "session_id", "employee_id", "employee_name", "score", "q1", "q2", 
                     "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "supervisor", 
                      "supervisor_id", "lob", "quality_auditor_id", "quality_auditor_name"
                ]               
            }
        },    
        "Walmart Exceptions": {
            "information_file": {
                "file_id": "1IDmxMYWkgCaP1bjF2LxXOwHo-qWTTr7yJuyrMoGTUe0",
                "file_url": "https://docs.google.com/spreadsheets/d/1IDmxMYWkgCaP1bjF2LxXOwHo-qWTTr7yJuyrMoGTUe0/edit?resourcekey=undefined#gid=1268877784",
            },
             "information_save_db": {
                "schema": "walmart",
                "table_name": "geo_exceptions",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Form Responses 1"]
                },
                "head": 1 
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Timestamp", "Email Address", "Agent Name", "Date of exception", "Start time of exception", 
                "End time of exception", "Exception category", "Additional notes", "Duration", "agent_name", 
                "emerge_id", "is_valid", "approved", "approver", "isduplicate"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_worksheet_google_form_responses_timestamp,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "Timestamp": "timestamp",
                    "Email Address": "email_address",                    
                    "Date of exception": "exception_date",
                    "Start time of exception": "start_of_exception",
                    "End time of exception": "end_of_exception",
                    "Exception category": "exception_category",
                    "Additional notes": "additional_notes",
                    "Duration": "duration_seconds",
                    "emerge_id": "legacy_id",
                    "approved": "approval_status"                    
                },
                "order_columns": [
                    "timestamp", "email_address", "agent_name", "exception_category", "additional_notes", 
                    "duration_seconds", "legacy_id", "is_valid", "approval_status", "approver", "exception_date", 
                    "start_of_exception", "end_of_exception"
                ],
                "validate_date_columns": {
                    "columns":[
                        "exception_date"
                    ]
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_of_exception", "end_of_exception"
                    ]
                },                
                "validate_duration_columns": {
                    "columns":  [
                        "duration_seconds"
                    ]
                },                             
                "validate_text_columns": [
                    "email_address", "agent_name", "exception_category", "additional_notes",
                    "legacy_id", "is_valid", "approval_status", "approver"
                ]                  
            }
        },
        #===========================================================================================
        #===========================================================================================
        "Henry Schein Honduras Training Manual Tracker": {
            "information_file": {
                "file_id": "1lC-XySFv7EFemu-NKPFOwEGRZ7yyAw2qtAr_E-y9QRI",
                "file_url": "https://docs.google.com/spreadsheets/d/1lC-XySFv7EFemu-NKPFOwEGRZ7yyAw2qtAr_E-y9QRI/edit#gid=903515930"
            },
            "information_save_db": {
                "schema": "henry_schein",
                "table_name": "sap_training_hour_tracker",
            },
            "information_extract_worksheets": {
                "method": {
                    "ignore_worksheets": ["Directory", "Validation"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.handling_worksheets_add_source_tab_column,
            "expected_columns_for_stack": [
                "agent_name_id", "date", "schedule", "week_shift_type", "real_regular_start_time", 
                "real_regular_end_time", "lunch_hours", "ot_hours_am (5AM - 7PM)", 
                "ot_hours_mix (7:01 PM - 10 PM)", "ot_hours_pm (10:01 PM - 5 AM)", 
                "regular_hours_worked", "is_valid", "agent_name", "legacy_id", 
                "schedule_start", "schedule_end", "scheduled_hours", "source_tab"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_honduras_manual_trackers,
            "grand_sheet_handling_todo": {
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_text_columns": [
                    "schedule", "week_shift_type", "agent_name", "legacy_id"
                ],
                "validate_datetime_columns": {
                    "columns":  [
                        "real_regular_start_time", "real_regular_end_time"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_hours", "ot_hours_am (5AM - 7PM)", "ot_hours_mix (7:01 PM - 10 PM)", 
                        "ot_hours_pm (10:01 PM - 5 AM)", "regular_hours_worked", "scheduled_hours"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "rename_columns": {
                    "lunch_hours": "lunch_sec",
                    "ot_hours_am (5AM - 7PM)": "ot_am_sec",
                    "ot_hours_mix (7:01 PM - 10 PM)": "ot_mix_sec",
                    "ot_hours_pm (10:01 PM - 5 AM)": "ot_pm_sec",
                    "regular_hours_worked": "time_worked_sec",
                    "scheduled_hours": "scheduled_sec"
                },
                "strip_string_columns":{
                    "flag"
                },                
                "order_columns": [
                    "agent_name", "legacy_id", "date", "schedule",
                    "week_shift_type", "real_regular_start_time", 
                    "real_regular_end_time", "lunch_sec", "ot_am_sec",  
                    "ot_mix_sec", "ot_pm_sec", "time_worked_sec", "source_tab", 
                    "flag", "schedule_start", "schedule_end", "scheduled_sec"
                ]
            }
        },
        #===========================================================================================
        #===========================================================================================
        "Henry Schein Honduras Operations Manual Tracker": {
            "information_file": {
                "file_id": "1k7-CZH3dZt7BdrzNMm-M_WGWQFz9jsYln1Ko4kJQ8TY",
                "file_url": "https://docs.google.com/spreadsheets/d/1k7-CZH3dZt7BdrzNMm-M_WGWQFz9jsYln1Ko4kJQ8TY/edit#gid=903515930"
            },
            "information_save_db": {
                "schema": "henry_schein",
                "table_name": "sap_operations_hour_tracker"
            },
            "information_extract_worksheets": {
                "method": {
                    "ignore_worksheets": ["Directory", "Validation"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.handling_worksheets_add_source_tab_column,
            "expected_columns_for_stack": [
                "agent_name_id", "date", "schedule", "week_shift_type", "real_regular_start_time", 
                "real_regular_end_time", "lunch_hours", "ot_hours_am (5AM - 7PM)", 
                "ot_hours_mix (7:01 PM - 10 PM)", "ot_hours_pm (10:01 PM - 5 AM)", 
                "regular_hours_worked", "is_valid", "agent_name", "legacy_id", 
                "schedule_start", "schedule_end", "scheduled_hours", "source_tab"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_honduras_manual_trackers,
            "grand_sheet_handling_todo": {
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_text_columns": [
                    "schedule", "week_shift_type", "agent_name", "legacy_id"
                ],
                "validate_datetime_columns": {
                    "columns":  [
                        "real_regular_start_time", "real_regular_end_time"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_hours", "ot_hours_am (5AM - 7PM)", "ot_hours_mix (7:01 PM - 10 PM)", 
                        "ot_hours_pm (10:01 PM - 5 AM)", "regular_hours_worked", "scheduled_hours"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "rename_columns": {
                    "lunch_hours": "lunch_sec",
                    "ot_hours_am (5AM - 7PM)": "ot_am_sec",
                    "ot_hours_mix (7:01 PM - 10 PM)": "ot_mix_sec",
                    "ot_hours_pm (10:01 PM - 5 AM)": "ot_pm_sec",
                    "regular_hours_worked": "time_worked_sec",
                    "scheduled_hours": "scheduled_sec"
                },
                "strip_string_columns":{
                    "flag"
                },                
                "order_columns": [
                    "agent_name", "legacy_id", "date", "schedule",
                    "week_shift_type", "real_regular_start_time", 
                    "real_regular_end_time", "lunch_sec", "ot_am_sec",  
                    "ot_mix_sec", "ot_pm_sec", "time_worked_sec", "source_tab", 
                    "flag", "schedule_start", "schedule_end", "scheduled_sec"
                ]
            }
        },
        #===========================================================================================
        #===========================================================================================   
        "Walmart Training Tracker": {
            "information_file": {
                "file_id": "1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw",
                "file_url": "https://docs.google.com/spreadsheets/d/1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw/edit#gid=1618029308",
            },
             "information_save_db": {
                "schema": "walmart",
                "table_name": "geo_manual_tracker_training",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Walmart"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },              
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                 
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },
        #===========================================================================================
        #===========================================================================================   
        "Harry and David Operations Tracker": {
            "information_file": {
                "file_id": "1lvwcjW3wF0CbsLf06dq4fVWJxmt7znSvgVDCn4xv98A",
                "file_url": "https://docs.google.com/spreadsheets/d/1lvwcjW3wF0CbsLf06dq4fVWJxmt7znSvgVDCn4xv98A/edit#gid=996711426",
            },
             "information_save_db": {
                "schema": "harry_and_david",
                "table_name": "geo_manual_tracker_operations",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Hour_Tracker"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },              
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                 
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },
        #===========================================================================================
        #===========================================================================================   
        "Kroger Operations Tracker": {
            "information_file": {
                "file_id": "1xDYYmFNEbFU5nc5iDfaNpI_eMVD9f6aP07JtZHvdz2o",
                "file_url": "https://docs.google.com/spreadsheets/d/1xDYYmFNEbFU5nc5iDfaNpI_eMVD9f6aP07JtZHvdz2o/edit#gid=996711426",
            },
             "information_save_db": {
                "schema": "kroger",
                "table_name": "geo_manual_tracker_operations",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Hour_Tracker"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },              
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                 
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },
        #===========================================================================================
        #===========================================================================================   
        "Harry and David Training Tracker": {
            "information_file": {
                "file_id": "1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw",
                "file_url": "https://docs.google.com/spreadsheets/d/1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw/edit#gid=1618029308",
            },
             "information_save_db": {
                "schema": "harry_and_david",
                "table_name": "geo_manual_tracker_training",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Harry and David"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },              
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                 
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },
        #===========================================================================================
        #===========================================================================================   
        "Kroger Training Tracker": {
            "information_file": {
                "file_id": "1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw",
                "file_url": "https://docs.google.com/spreadsheets/d/1JFeDiTHweFFhN8QUyKSVfTgshLWtM1d3dtuDgvvHuFw/edit#gid=1618029308",
            },
             "information_save_db": {
                "schema": "kroger",
                "table_name": "geo_manual_tracker_training",
            },
            "information_extract_worksheets": {
               "method": {
                    "extract_worksheets": ["Kroger"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.pass_function_worksheets,
            "expected_columns_for_stack": [
                "Agent_Name_ID", "Date", "Start_Shift", "End_Shift", "Lunch_Time", "Hours_Worked", "Is_Valid", "Agent_Name", "AgentID"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_guyana_training_tracker,
            "grand_sheet_handling_todo": {
                "rename_columns": {
                    "agentid": "legacy_id",
                    "hours_worked":"worked_time_sec",
                    "lunch_time":"lunch_time_sec"
                },              
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_datetime_columns": {
                    "columns":  [
                        "start_shift", "end_shift"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_time_sec", "worked_time_sec"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },                 
                "validate_text_columns": [
                    "agent_name", "legacy_id", 
                ],                
                "order_columns": [
                    "agent_name", "date", "start_shift", "end_shift", "lunch_time_sec", "worked_time_sec", "agent_name_id", "legacy_id",
                    "flag", "the_index"
                ]                
            }
        },
        #===========================================================================================
        #===========================================================================================
        "GOALS Honduras Training Manual Tracker": {
            "information_file": {
                "file_id": "1bxZ1dpHt4x5w_nEk-CedWFFJJhGTOrTxrys9TpNdBSc",
                "file_url": "https://docs.google.com/spreadsheets/d/1bxZ1dpHt4x5w_nEk-CedWFFJJhGTOrTxrys9TpNdBSc/edit#gid=0"
            },
            "information_save_db": {
                "schema": "goals",
                "table_name": "sap_training_hour_tracker"
            },
            "information_extract_worksheets": {
                "method": {
                    "ignore_worksheets": ["Directory", "Validation", "Hour Checker", "Hour Compiler"]
                },
                "head": 2
            }, 
            "handling_worksheets": gshw.handling_worksheets_add_source_tab_column,
            "expected_columns_for_stack": [
                "agent_name_id", "date", "schedule", "week_shift_type", "real_regular_start_time", 
                "real_regular_end_time", "lunch_hours", "ot_hours_am (5AM - 7PM)", 
                "ot_hours_mix (7:01 PM - 10 PM)", "ot_hours_pm (10:01 PM - 5 AM)", 
                "regular_hours_worked", "is_valid", "agent_name", "legacy_id", 
                "schedule_start", "schedule_end", "scheduled_hours", "source_tab"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_honduras_manual_trackers,
            "grand_sheet_handling_todo": {
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_text_columns": [
                    "schedule", "week_shift_type", "agent_name", "legacy_id"
                ],
                "validate_datetime_columns": {
                    "columns":  [
                        "real_regular_start_time", "real_regular_end_time"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_hours", "ot_hours_am (5AM - 7PM)", "ot_hours_mix (7:01 PM - 10 PM)", 
                        "ot_hours_pm (10:01 PM - 5 AM)", "regular_hours_worked", "scheduled_hours"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "rename_columns": {
                    "lunch_hours": "lunch_sec",
                    "ot_hours_am (5AM - 7PM)": "ot_am_sec",
                    "ot_hours_mix (7:01 PM - 10 PM)": "ot_mix_sec",
                    "ot_hours_pm (10:01 PM - 5 AM)": "ot_pm_sec",
                    "regular_hours_worked": "time_worked_sec",
                    "scheduled_hours": "scheduled_sec"
                },
                "strip_string_columns":{
                    "flag"
                },                
                "order_columns": [
                    "agent_name", "legacy_id", "date", "schedule",
                    "week_shift_type", "real_regular_start_time", 
                    "real_regular_end_time", "lunch_sec", "ot_am_sec",  
                    "ot_mix_sec", "ot_pm_sec", "time_worked_sec", "source_tab", 
                    "flag", "schedule_start", "schedule_end", "scheduled_sec"
                ]
            }
        },
        #===========================================================================================
        #===========================================================================================       
        "GOALS Honduras Operations Manual Tracker": {
            "information_file": {
                "file_id": "1fTvSc-qW1S1Ei8jZQAikKMPCcPRQE_1E1h8YEzuIrRI",
                "file_url": "https://docs.google.com/spreadsheets/d/1fTvSc-qW1S1Ei8jZQAikKMPCcPRQE_1E1h8YEzuIrRI/edit#gid=0",
            },
            "information_save_db": {
                "schema": "goals",
                "table_name": "sap_operations_hour_tracker"
            },
            "information_extract_worksheets": {
                "method": {
                    "ignore_worksheets": ["Directory", "Validation"]
                },
                "head": 2
            },
            "handling_worksheets": gshw.handling_worksheets_add_source_tab_column,
            "expected_columns_for_stack": [
                "agent_name_id", "date", "schedule", "week_shift_type", "real_regular_start_time", 
                "real_regular_end_time", "lunch_hours", "ot_hours_am (5AM - 7PM)", 
                "ot_hours_mix (7:01 PM - 10 PM)", "ot_hours_pm (10:01 PM - 5 AM)", 
                "regular_hours_worked", "is_valid", "agent_name", "legacy_id", 
                "schedule_start", "schedule_end", "scheduled_hours", "source_tab"
            ],
            "handling_grand_worksheet": lgsh_functions_lib.handling_grand_worksheet_honduras_manual_trackers,
            "grand_sheet_handling_todo": {
                "validate_date_columns": {
                    "columns":[
                        "date"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_text_columns": [
                    "schedule", "week_shift_type", "agent_name", "legacy_id"
                ],
                "validate_datetime_columns": {
                    "columns":  [
                        "real_regular_start_time", "real_regular_end_time"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "validate_duration_columns": {
                    "columns":  [
                        "lunch_hours", "ot_hours_am (5AM - 7PM)", "ot_hours_mix (7:01 PM - 10 PM)", 
                        "ot_hours_pm (10:01 PM - 5 AM)", "regular_hours_worked", "scheduled_hours"
                    ],
                    "parameters": {
                        "raise_flag": "true"
                    }
                },
                "rename_columns": {
                    "lunch_hours": "lunch_sec",
                    "ot_hours_am (5AM - 7PM)": "ot_am_sec",
                    "ot_hours_mix (7:01 PM - 10 PM)": "ot_mix_sec",
                    "ot_hours_pm (10:01 PM - 5 AM)": "ot_pm_sec",
                    "regular_hours_worked": "time_worked_sec",
                    "scheduled_hours": "scheduled_sec"
                },
                "strip_string_columns":{
                    "flag"
                },                
                "order_columns": [
                    "agent_name", "legacy_id", "date", "schedule",
                    "week_shift_type", "real_regular_start_time", 
                    "real_regular_end_time", "lunch_sec", "ot_am_sec",  
                    "ot_mix_sec", "ot_pm_sec", "time_worked_sec", "source_tab", 
                    "flag", "schedule_start", "schedule_end", "scheduled_sec"
                ]
            }
        },        
    }
    
}