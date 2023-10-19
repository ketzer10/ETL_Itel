import src.office_depot.functions.report_manager_functions as transforms_function
import utils.utils as utils
configs = {
    "office_depot_geo_actual_forecast":{
        "read_with_dtype":{
            "FcstName3":"str", 
            "PostedCalls5":"str", 
            "Textbox46":"str", 
            "Textbox48":"str", 
            "LockedCalls6":"str", 
            "Textbox39":"str", 
            "Textbox41":"str", 
            "Textbox117":"str", 
            "SDate2":"str", 
            "PostedCalls3":"str", 
            "Textbox19":"str", 
            "Textbox24":"str", 
            "LockedCalls4":"str", 
            "Textbox36":"str", 
            "Textbox37":"str", 
            "Textbox63":"str", 
            "PostedHead3":"str", 
            "Textbox44":"str", 
            "LockedHead2":"str", 
            "Textbox21":"str", 
            "ActualTm5":"str", 
            "Textbox27":"str", 
            "ActualHead4":"str", 
            "ActualHead6":"str", 
            "ActualAbnAll2":"str", 
            "HalfHourOfDay3":"str", 
            "PostedCalls9":"str", 
            "Textbox213":"str", 
            "Textbox214":"str", 
            "LockedCalls10":"str", 
            "ActualCalls4":"str", 
            "Textbox215":"str", 
            "Textbox216":"str", 
            "PostedHead7":"str", 
            "Textbox217":"str", 
            "LockedHead6":"str", 
            "Textbox218":"str", 
            "ActualTm11":"str", 
            "Textbox219":"str", 
            "ActualHead12":"str", 
            "ActualHead13":"str", 
            "Textbox220":"str", 
            "ActualAbnAll6":"str"            
        },  
        "delete_insert_keys": ["date", "channel"],
        "info_transform_function":{
            "output_columns":  ["channel", "date", "posted_volume", "uncommited_volume",  
                            "locked_volume", "actual_volume_offered", "actual_volume_answered", "volume_variance", 
                            "posted_hc", "variance_posted_hc", "locked_hc_avg", "locked_staff_hours", 
                            "locked_staff_hr_connected_available", "variance_staff_hours", "actual_calculated_hc", 
                            "variance_calculated_hc", "abandons"],            
            "df_handling": {
                        "validate_float_columns":{
                            "posted_volume", "uncommited_volume",  
                            "locked_volume", "actual_volume_offered", "actual_volume_answered", "volume_variance", 
                            "posted_hc", "variance_posted_hc", "locked_hc_avg", "locked_staff_hours", 
                            "locked_staff_hr_connected_available", "variance_staff_hours", "actual_calculated_hc", 
                            "variance_calculated_hc", "abandons"
                        },
                        "validate_date_columns":{
                            "columns":["date"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    }
            },
        "transform_function" : transforms_function.forecast_actuals_transform
    },
    "office_depot_external_qa_bsd":{
        "read_with_dtype":{
            "Textbox32":"str", 
            "SiteName":"str", 
            "Textbox1":"str", 
            "SDate":"str", 
            "Textbox36":"str", 
            "SessionID":"str", 
            "Textbox16":"str", 
            "QuestionSection1":"str", 
            "PointsEarned1":"str", 
            "PointsEarned2":"str", 
            "QuestionText":"str", 
            "Answer":"str", 
            "PointsEarned":"str", 
            "PointsPossibleDisplay":"str", 
            "Textbox2":"str"           
        },  
        "delete_insert_keys": ["sessionid"],
        "info_transform_function":{
            "output_columns":  ["channel", "date", "posted_volume", "uncommited_volume",  
                            "locked_volume", "actual_volume_offered", "actual_volume_answered", "volume_variance", 
                            "posted_hc", "variance_posted_hc", "locked_hc_avg", "locked_staff_hours", 
                            "locked_staff_hr_connected_available", "variance_staff_hours", "actual_calculated_hc", 
                            "variance_calculated_hc", "abandons"],            
            "df_handling": {
                        "validate_float_columns":{
                            "final_score", "points_earned_connect", "points_earned_easy", "points_earned_resolution", 
                            "points_possible_connect", "points_possible_easy", "points_possible_resolution"
                        },
                        "validate_date_columns":{
                            "columns":["date"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    },
            "lob":"BSD"
            },
        "transform_function" : transforms_function.office_depot_external_qa
    },
    "office_depot_external_qa_billing":{
        "read_with_dtype":{
            "Textbox32":"str", 
            "SiteName":"str", 
            "Textbox1":"str", 
            "SDate":"str", 
            "Textbox36":"str", 
            "SessionID":"str", 
            "Textbox16":"str", 
            "QuestionSection1":"str", 
            "PointsEarned1":"str", 
            "PointsEarned2":"str", 
            "QuestionText":"str", 
            "Answer":"str", 
            "PointsEarned":"str", 
            "PointsPossibleDisplay":"str", 
            "Textbox2":"str"           
        },  
        "delete_insert_keys": ["sessionid"],
        "info_transform_function":{
            "output_columns":  ["channel", "date", "posted_volume", "uncommited_volume",  
                            "locked_volume", "actual_volume_offered", "actual_volume_answered", "volume_variance", 
                            "posted_hc", "variance_posted_hc", "locked_hc_avg", "locked_staff_hours", 
                            "locked_staff_hr_connected_available", "variance_staff_hours", "actual_calculated_hc", 
                            "variance_calculated_hc", "abandons"],            
            "df_handling": {
                        "validate_float_columns":{
                            "final_score", "points_earned_connect", "points_earned_easy", "points_earned_resolution", 
                            "points_possible_connect", "points_possible_easy", "points_possible_resolution"
                        },
                        "validate_date_columns":{
                            "columns":["date"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    },
            "lob":"Billing"
            },
        "transform_function" : transforms_function.office_depot_external_qa
    },
    "office_depot_external_qa_chat":{
        "read_with_dtype":{
            "Textbox32":"str", 
            "SiteName":"str", 
            "Textbox1":"str", 
            "SDate":"str", 
            "Textbox36":"str", 
            "SessionID":"str", 
            "Textbox16":"str", 
            "QuestionSection1":"str", 
            "PointsEarned1":"str", 
            "PointsEarned2":"str", 
            "QuestionText":"str", 
            "Answer":"str", 
            "PointsEarned":"str", 
            "PointsPossibleDisplay":"str", 
            "Textbox2":"str"           
        },  
        "delete_insert_keys": ["sessionid"],
        "info_transform_function":{
            "output_columns":  ["channel", "date", "posted_volume", "uncommited_volume",  
                            "locked_volume", "actual_volume_offered", "actual_volume_answered", "volume_variance", 
                            "posted_hc", "variance_posted_hc", "locked_hc_avg", "locked_staff_hours", 
                            "locked_staff_hr_connected_available", "variance_staff_hours", "actual_calculated_hc", 
                            "variance_calculated_hc", "abandons"],            
            "df_handling": {
                        "validate_float_columns":{
                            "final_score", "points_earned_connect", "points_earned_easy", "points_earned_resolution", 
                            "points_possible_connect", "points_possible_easy", "points_possible_resolution"
                        },
                        "validate_date_columns":{
                            "columns":["date"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    },
            "lob":"Chat"
            },
        "transform_function" : transforms_function.office_depot_external_qa
    },
    "office_depot_external_qa_contract":{
        "read_with_dtype":{
            "Textbox32":"str", 
            "SiteName":"str", 
            "Textbox1":"str", 
            "SDate":"str", 
            "Textbox36":"str", 
            "SessionID":"str", 
            "Textbox16":"str", 
            "QuestionSection1":"str", 
            "PointsEarned1":"str", 
            "PointsEarned2":"str", 
            "QuestionText":"str", 
            "Answer":"str", 
            "PointsEarned":"str", 
            "PointsPossibleDisplay":"str", 
            "Textbox2":"str"           
        },  
        "delete_insert_keys": ["sessionid"],
        "info_transform_function":{
            "output_columns":  ["channel", "date", "posted_volume", "uncommited_volume",  
                            "locked_volume", "actual_volume_offered", "actual_volume_answered", "volume_variance", 
                            "posted_hc", "variance_posted_hc", "locked_hc_avg", "locked_staff_hours", 
                            "locked_staff_hr_connected_available", "variance_staff_hours", "actual_calculated_hc", 
                            "variance_calculated_hc", "abandons"],            
            "df_handling": {
                        "validate_float_columns":{
                            "final_score", "points_earned_connect", "points_earned_easy", "points_earned_resolution", 
                            "points_possible_connect", "points_possible_easy", "points_possible_resolution"
                        },
                        "validate_date_columns":{
                            "columns":["date"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    },
            "lob":"Contract"
            },
        "transform_function" : transforms_function.office_depot_external_qa
    },
    "office_depot_external_qa_direct":{
        "read_with_dtype":{
            "Textbox32":"str", 
            "SiteName":"str", 
            "Textbox1":"str", 
            "SDate":"str", 
            "Textbox36":"str", 
            "SessionID":"str", 
            "Textbox16":"str", 
            "QuestionSection1":"str", 
            "PointsEarned1":"str", 
            "PointsEarned2":"str", 
            "QuestionText":"str", 
            "Answer":"str", 
            "PointsEarned":"str", 
            "PointsPossibleDisplay":"str", 
            "Textbox2":"str"           
        },  
        "delete_insert_keys": ["sessionid"],
        "info_transform_function":{
            "output_columns":  ["channel", "date", "posted_volume", "uncommited_volume",  
                            "locked_volume", "actual_volume_offered", "actual_volume_answered", "volume_variance", 
                            "posted_hc", "variance_posted_hc", "locked_hc_avg", "locked_staff_hours", 
                            "locked_staff_hr_connected_available", "variance_staff_hours", "actual_calculated_hc", 
                            "variance_calculated_hc", "abandons"],            
            "df_handling": {
                        "validate_float_columns":{
                            "final_score", "points_earned_connect", "points_earned_easy", "points_earned_resolution", 
                            "points_possible_connect", "points_possible_easy", "points_possible_resolution"
                        },
                        "validate_date_columns":{
                            "columns":["date"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    },
            "lob":"Direct"
            },
        "transform_function" : transforms_function.office_depot_external_qa
    },
    "office_depot_external_qa_ecom":{
        "read_with_dtype":{
            "Textbox32":"str", 
            "SiteName":"str", 
            "Textbox1":"str", 
            "SDate":"str", 
            "Textbox36":"str", 
            "SessionID":"str", 
            "Textbox16":"str", 
            "QuestionSection1":"str", 
            "PointsEarned1":"str", 
            "PointsEarned2":"str", 
            "QuestionText":"str", 
            "Answer":"str", 
            "PointsEarned":"str", 
            "PointsPossibleDisplay":"str", 
            "Textbox2":"str"           
        },  
        "delete_insert_keys": ["sessionid"],
        "info_transform_function":{
            "output_columns":  ["channel", "date", "posted_volume", "uncommited_volume",  
                            "locked_volume", "actual_volume_offered", "actual_volume_answered", "volume_variance", 
                            "posted_hc", "variance_posted_hc", "locked_hc_avg", "locked_staff_hours", 
                            "locked_staff_hr_connected_available", "variance_staff_hours", "actual_calculated_hc", 
                            "variance_calculated_hc", "abandons"],            
            "df_handling": {
                        "validate_float_columns":{
                            "final_score", "points_earned_connect", "points_earned_easy", "points_earned_resolution", 
                            "points_possible_connect", "points_possible_easy", "points_possible_resolution"
                        },
                        "validate_date_columns":{
                            "columns":["date"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    },
            "lob":"Ecom"
            },
        "transform_function" : transforms_function.office_depot_external_qa
    },
    "od_customer_service":{
        "read_with_dtype":{
            "Textbox32":"str", 
            "SiteName":"str", 
            "Textbox1":"str", 
            "SDate":"str", 
            "Textbox36":"str", 
            "SessionID":"str", 
            "Textbox16":"str", 
            "QuestionSection1":"str", 
            "PointsEarned1":"str", 
            "PointsEarned2":"str", 
            "QuestionText":"str", 
            "Answer":"str", 
            "PointsEarned":"str", 
            "PointsPossibleDisplay":"str", 
            "Textbox2":"str"           
        },  
        "delete_insert_keys": ["sessionid"],
        "info_transform_function":{
            "output_columns":  ["channel", "date", "posted_volume", "uncommited_volume",  
                            "locked_volume", "actual_volume_offered", "actual_volume_answered", "volume_variance", 
                            "posted_hc", "variance_posted_hc", "locked_hc_avg", "locked_staff_hours", 
                            "locked_staff_hr_connected_available", "variance_staff_hours", "actual_calculated_hc", 
                            "variance_calculated_hc", "abandons"],            
            "df_handling": {
                        "validate_float_columns":{
                            "final_score", "points_earned_connect", "points_earned_easy", "points_earned_resolution", 
                            "points_possible_connect", "points_possible_easy", "points_possible_resolution"
                        },
                        "validate_date_columns":{
                            "columns":["date"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    }
            },
        "transform_function" : transforms_function.office_depot_external_qa
    },
    "office_depot_team_time":{
        "read_with_dtype":{
            "AgentID3":"str", 
            "AgentName2":"str", 
            "StaffHours1":"str", 
            "TotalTime1":"str", 
            "CallCt1":"str", 
            "IdleTime1":"str", 
            "IdleLunch1":"str", 
            "IdleBreak1":"str", 
            "IdleCall1":"str", 
            "IdleCoach1":"str", 
            "IdleTrain1":"str", 
            "IdleMeeting1":"str", 
            "IdleSpec1":"str", 
            "IdleOBP1":"str", 
            "IdleOther1":"str", 
            "AvailableTime1":"str", 
            "HoldCount1":"str", 
            "HoldTm1":"str", 
            "ConnectedTime":"str", 
            "WrapTime1":"str", 
            "RingTime1":"str", 
            "NotRespTime1":"str", 
            "SDate":"str", 
            "TeamName":"str", 
            "StaffHours":"str", 
            "TotalTime":"str", 
            "CallCt":"str", 
            "IdleTime":"str", 
            "IdleLunch":"str", 
            "IdleBreak":"str", 
            "IdleCall":"str", 
            "IdleCoach":"str", 
            "IdleTrain":"str", 
            "IdleMeeting":"str", 
            "IdleSpec":"str", 
            "IdleOBP":"str", 
            "IdleOther":"str", 
            "AvailableTime":"str", 
            "HoldCount":"str", 
            "HoldTm":"str", 
            "HandleTime":"str", 
            "WrapTime":"str", 
            "RingTime":"str", 
            "NotRespTime":"str"          
        },  
        "delete_insert_keys": ["thedate", "team_name"],
        "info_transform_function":{
            "output_columns":  [],            
            "df_handling": {
                        "validate_float_columns":{
                            "staff_hours","total_time", "call_count", "idle_time", "idle_lunch", "idle_break",
                            "acw_hours", "idle_coach", "idle_train", "idle_meeting", "idle_spec",
                            "idle_obp", "idle_other", "available_time", "hold_count", "hold_time",
                            "handle_time", "wrap_time", "ring_time", "not_resp_time"
                        },
                        "validate_date_columns":{
                            "columns":["thedate"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    }
            },
        "transform_function" : transforms_function.agent_activity_team_time
    },  
    "office_depot_cjp_agent_summary":{
        "read_with_dtype":{
            "Agent":"str", 
            "Date":"str", 
            "Channel":"str", 
            "Login Count":"str", 
            "Calls Handled":"str", 
            "Staff Hours":"str", 
            "Initial Login Time":"str", 
            "Final Logout Time":"str", 
            "Occupancy":"str", 
            "Idle Count":"str", 
            "Total Idle Time":"str", 
            "Average Idle Time":"str", 
            "Available Count":"str", 
            "Total Available Time":"str", 
            "Average Available Tim":"str", 
            "Inbound Reserved Count":"str", 
            "Total Inbound Reserved Time":"str", 
            "Average Inbound Reserved Time":"str", 
            "Inbound Hold Count":"str", 
            "Inbound Connected Count":"str", 
            "Total Inbound Talk Time":"str", 
            "Total Inbound Hold Time":"str", 
            "Total Inbound Connected Time":"str", 
            "Average Inbound Hold Time":"str", 
            "Average Inbound Connected Time":"str", 
            "OutDial Reserved Count":"str", 
            "Total OutDial Reserved Time":"str", 
            "Average OutDial Reserved Time":"str", 
            "Outdial Attempted Count":"str", 
            "Outdial Connected Count":"str", 
            "Outdial Hold Count":"str", 
            "Total Outdial Talk Time":"str", 
            "Total Outdial Hold Time":"str", 
            "Total Outdial Connected Time":"str", 
            "Average Outdial Hold Time":"str", 
            "Average Outdial Connected Time":"str", 
            "Disconnected Count":"str", 
            "Inbound Wrap Up Count":"str", 
            "Total Inbound Wrap Up Time":"str", 
            "Average Inbound Wrap Up Time":"str", 
            "Outdial Wrap Up Count":"str", 
            "Total Outdial Wrap Up time":"str", 
            "Average Outdial Wrap Up Time":"str", 
            "Not Responding Count":"str", 
            "Total Not Responding Time":"str", 
            "Average Not Responding Time":"str", 
            "Consult Answer Count":"str", 
            "Total Consult Answer Time":"str", 
            "Average Consult Answer Time":"str", 
            "Consult Request Count":"str", 
            "Total Consult Request Time":"str", 
            "Average Consult Request Time":"str", 
            "Consult Count":"str", 
            "Total Consult Time":"str", 
            "Average Consult Time":"str", 
            "Conference":"str", 
            "Inbound CTQ Request Count":"str", 
            "Total Inbound CTQ Request Time":"str", 
            "Inbound CTQ Answer Count":"str", 
            "Total Inbound CTQ Answer Time":"str", 
            "Outdial CTQ Request Count":"str", 
            "Total Outdial CTQ Request Time":"str", 
            "Outdial CTQ Answer Count":"str", 
            "Total Outdial CTQ Answer Time":"str", 
            "Agent Transfer":"str", 
            "Agent Requeue":"str", 
            "Blind Transfer":"str", 
            "Inbound Avg Handle Time":"str", 
            "Outdial Avg Handle Time":"str"         
        },  
        "delete_insert_keys": ["date", "agent_id"],
        "info_transform_function":{
            "output_columns":  ["agent_id", "date", "staff_sec", "initial_login_time", "final_logout_time", 
                                "total_available_time_sec", "total_inbound_talk_time_sec", "total_inbound_hold_time_sec", 
                                "total_inbound_connected_time_sec", "total_outdial_talk_time_sec", "total_outdial_hold_time_sec", 
                                "total_outdial_connected_time_sec", "total_inbound_wrap_up_time_sec", "total_outdial_wrap_up_time_sec", 
                                "calls_handled"],            
            "df_handling": {
                        "validate_float_columns":{
                            "total_available_time_sec", "total_inbound_talk_time_sec", "total_inbound_hold_time_sec", 
                            "total_inbound_connected_time_sec", "total_outdial_talk_time_sec", "total_outdial_hold_time_sec", 
                            "total_outdial_connected_time_sec", "total_inbound_wrap_up_time_sec", "total_outdial_wrap_up_time_sec", 
                            "calls_handled"
                        },
                        "validate_date_columns":{
                            "columns":["date"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    }
            },
        "transform_function" : transforms_function.office_depot_cjp_agent_summary
    },    
    "office_depot_cjp_calls_handled_queue":{
        "read_with_dtype":{
            "Queue":"str", 
            "Site":"str", 
            "Team":"str", 
            "Date":"str", 
            "Completed ":"str", 
            "Disconnected":"str", 
            "Transferred":"str", 
            "Transferred Out":"str", 
            "Blind Transfers":"str", 
            "Requeued":"str", 
            "Answered":"str", 
            "Secondary Answered":"str", 
            "Consult Count":"str", 
            "CTQ Request Count":"str", 
            "Conference Count":"str", 
            "Hold Count":"str"      
        },  
        "delete_insert_keys": ["thedate", "team"],
        "info_transform_function":{
            "output_columns":  ["queue", "site", "team", "thedate", "completed", "disconnected", "transferred", "transferred_out", 
                                "blind_transfers", "requeued", "answered", "secondary_answered", "consult_count", "ctq_request_count", 
                                "conference_count", "hold_count"],            
            "df_handling": {
                        "validate_float_columns":{
                                "completed", "disconnected", "transferred", "transferred_out", 
                                "blind_transfers", "requeued", "answered", "secondary_answered", "consult_count", "ctq_request_count", 
                                "conference_count", "hold_count"
                        },
                        "validate_date_columns":{
                            "columns":["thedate"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    }
            },
        "transform_function" : transforms_function.office_depot_cjp_calls_handled_queue
    },
    "od_customer_service_detail":{
        "read_with_dtype":{
            "Textbox32":"str", 
            "SiteName":"str", 
            "Textbox1":"str", 
            "SDate":"str", 
            "Textbox36":"str", 
            "SessionID":"str", 
            "Textbox16":"str", 
            "QuestionSection1":"str", 
            "PointsEarned1":"str", 
            "PointsEarned2":"str", 
            "QuestionText":"str", 
            "Answer":"str", 
            "PointsEarned":"str", 
            "PointsPossibleDisplay":"str", 
            "Textbox2":"str"           
        },  
        "delete_insert_keys": ["sessionid"],
        "info_transform_function":{
            "output_columns":  ["channel", "date", "posted_volume", "uncommited_volume",  
                            "locked_volume", "actual_volume_offered", "actual_volume_answered", "volume_variance", 
                            "posted_hc", "variance_posted_hc", "locked_hc_avg", "locked_staff_hours", 
                            "locked_staff_hr_connected_available", "variance_staff_hours", "actual_calculated_hc", 
                            "variance_calculated_hc", "abandons"],            
            "df_handling": {
                        "validate_date_columns":{
                            "columns":["date"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    }
            },
        "transform_function" : transforms_function.office_depot_external_qa},
    "od_crm_daily_phone":{
        "read_with_dtype":{
            "ResponseCnt3":"str", 
            "Textbox56":"str", 
            "Textbox37":"str", 
            "Textbox38":"str", 
            "Textbox39":"str", 
            "Textbox40":"str", 
            "Mnth1":"str", 
            "ResponseCnt2":"str", 
            "Textbox53":"str", 
            "Textbox128":"str", 
            "Textbox129":"str", 
            "Textbox130":"str", 
            "Textbox6":"str", 
            "Wk1":"str", 
            "ResponseCnt1":"str", 
            "Textbox54":"str", 
            "Textbox115":"str", 
            "Textbox116":"str", 
            "Textbox117":"str", 
            "Textbox8":"str", 
            "SDate":"str", 
            "ResponseCnt":"str", 
            "Textbox55":"str", 
            "Textbox103":"str", 
            "Textbox104":"str", 
            "Textbox105":"str", 
            "Textbox10":"str", 
            "NTLogon1":"str", 
            "ResponseCnt5":"str", 
            "Textbox65":"str", 
            "Textbox108":"str", 
            "Textbox109":"str", 
            "Textbox110":"str", 
            "Textbox23":"str", 
            "QueueName":"str", 
            "Q1":"str", 
            "Q2":"str", 
            "Q3":"str", 
            "Q4":"int", 
            "Comments":"str", 
            "SessionID":"str", 
            "Reference":"str"           
        },  
        "delete_insert_keys": ["reference"],
        "info_transform_function":{
            "output_columns":  ["date","agent_name","office_depot_id","aops_id","reference",
                                "connect_text","resolve_text","ease_text","ltr","queue_name",
                                "connect_score", "resolve_score", "ease_score", "promoters", "detractors",
                                "passives"],            
            "df_handling": {
                        "validate_date_columns":{
                            "columns":["date"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    }
            },
        "transform_function" : transforms_function.office_depot_crm_phones},
    "od_crm_daily_sms":{
        "read_with_dtype":{
            "ResponseCnt3":"str", 
            "Textbox56":"str", 
            "Textbox37":"str", 
            "Textbox38":"str", 
            "Textbox39":"str", 
            "Textbox40":"str", 
            "SiteName1":"str", 
            "Mnth1":"str", 
            "ResponseCnt2":"str", 
            "Textbox53":"str", 
            "Textbox128":"str", 
            "Textbox129":"str", 
            "Textbox130":"str", 
            "Textbox6":"str", 
            "Wk1":"str", 
            "ResponseCnt1":"str", 
            "Textbox54":"str", 
            "Textbox115":"str", 
            "Textbox116":"str", 
            "Textbox117":"str", 
            "Textbox8":"str", 
            "SDate":"str", 
            "ResponseCnt":"str", 
            "Textbox55":"str", 
            "Textbox103":"str", 
            "Textbox104":"str", 
            "Textbox105":"str", 
            "Textbox10":"str", 
            "NTLogon1":"str", 
            "ResponseCnt5":"str", 
            "Textbox65":"str", 
            "Textbox108":"str", 
            "Textbox109":"str", 
            "Textbox110":"str", 
            "Textbox23":"str", 
            "Reference":"str", 
            "Q1":"str", 
            "Q2":"str", 
            "Q3":"str", 
            "Q4":"int", 
            "Comments":"str", 
            "QueueName":"str", 
            "Reference1":"str", 
            "Reference2":"str"
        },
        "delete_insert_keys": ["reference"],
        "info_transform_function":{
            "output_columns":  ["date","agent_name","office_depot_id","aops_id","reference",
                                "connect_text","resolve_text","ease_text","ltr","queue_name",
                                "connect_score", "resolve_score", "ease_score", "promoters", "detractors",
                                "passives"],            
            "df_handling": {
                        "validate_date_columns":{
                            "columns":["date"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    }
            },   
        "transform_function" : transforms_function.office_depot_crm_sms           
    }, 
    "od_crm_daily_chat":{
        "read_with_dtype":{
            "ResponseCnt3":"str", 
            "Textbox56":"str", 
            "Textbox37":"str", 
            "Textbox38":"str", 
            "Textbox39":"str", 
            "Textbox40":"str", 
            "Mnth1":"str", 
            "ResponseCnt2":"str", 
            "Textbox53":"str", 
            "Textbox128":"str", 
            "Textbox129":"str", 
            "Textbox130":"str", 
            "Textbox6":"str", 
            "Wk1":"str", 
            "ResponseCnt1":"str", 
            "Textbox54":"str", 
            "Textbox115":"str", 
            "Textbox116":"str", 
            "Textbox117":"str", 
            "Textbox8":"str", 
            "SDate":"str", 
            "ResponseCnt":"str", 
            "Textbox55":"str", 
            "Textbox103":"str", 
            "Textbox104":"str", 
            "Textbox105":"str", 
            "Textbox10":"str", 
            "NTLogon1":"str", 
            "ResponseCnt5":"str", 
            "Textbox65":"str", 
            "Textbox108":"str", 
            "Textbox109":"str", 
            "Textbox110":"str", 
            "Textbox23":"str", 
            "Reference":"str", 
            "Q1":"str", 
            "Q2":"str", 
            "Q3":"str", 
            "Q4":"int", 
            "Comments":"str"
        },
        "delete_insert_keys": ["reference"],
        "info_transform_function":{
            "output_columns":  ["date","agent_name","office_depot_id","aops_id","reference",
                                "connect_text","resolve_text","ease_text","ltr","queue_name",
                                "connect_score", "resolve_score", "ease_score", "promoters", "detractors",
                                "passives"],            
            "df_handling": {
                        "validate_date_columns":{
                            "columns":["date"],
                            "parameters":{
                                "date_format":"%Y-%m-%d"
                            }
                        }                
                    }
            },   
        "transform_function" : transforms_function.office_depot_crm_chat         
    },     
}


