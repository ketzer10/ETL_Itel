kroger_productivity={
    # ======= Setup in old way to run script ==========================
        # "expected_columns":[
        #     'Agent Name','ACD Calls','Avg ACD Time','Avg ACW Time','% Agent Occupancy w/ ACW',                           # Expected columns in report
        #     '% Agent Occupancy w/o ACW','Extn In Calls','Avg Extn In Time','Extn Out Calls','Avg Extn Out Time',
        #     'ACD Time','ACW Time','Agent Ring Time','Other Time','AUX Time','Avail Time','Staffed Time','Lunch',
        #     'Break','Aux 10-99','Time in Misc','Date'],

        # "drop_columns":[
        #     'Lunch','Break','Aux 10-99','Time in Misc'],                                                                 # Columns to drop       
            
        # "headers":[
        #     'agent_name','acd_calls','avg_acd_time','avg_acw_time','agent_occupancy_with_acw_pct',
        #     'agent_occupancy_without_acw_pct','extn_in_calls','avg_extn_in_time','extn_out_calls',
        #     'avg_extn_out_time','acd_time','acw_time','agent_ring_time','other_time','aux_time','avail_time',
        #     'staffed_time','date'],

    # ======= Setup in new way to run script ==========================
        "df_handling": {
            "order_columns": [
                "Agent Name", "ACD Calls", "Avg ACD Time", "Avg ACW Time", "% Agent Occupancy w/ ACW", 
                "% Agent Occupancy w/o ACW", "Extn In Calls", "Avg Extn In Time", "Extn Out Calls", "Avg Extn Out Time",
                "ACD Time", "ACW Time", "Agent Ring Time", "Other Time", "AUX Time", "Avail Time", "Staffed Time", "Date" 
            ],
            "rename_columns": {
                "Agent Name": "agent_name", 
                "ACD Calls": "acd_calls", 
                "Avg ACD Time": "avg_acd_time", 
                "Avg ACW Time": "avg_acw_time", 
                "% Agent Occupancy w/ ACW": "agent_occupancy_with_acw_pct", 
                "% Agent Occupancy w/o ACW": "agent_occupancy_without_acw_pct", 
                "Extn In Calls": "extn_in_calls", 
                "Avg Extn In Time": "avg_extn_in_time", 
                "Extn Out Calls": "extn_out_calls", 
                "Avg Extn Out Time": "avg_extn_out_time",
                "ACD Time": "acd_time", 
                "ACW Time": "acw_time", 
                "Agent Ring Time": "agent_ring_time", 
                "Other Time": "other_time", 
                "AUX Time": "aux_time", 
                "Avail Time": "avail_time", 
                "Staffed Time": "staffed_time", 
                "Date": "date"
            }
        },  
        "keys":[
            "date"
        ]
    }

csat={

        "expected_columns" : [ 
            'Responded Date (Trim)','Line of Business','Case Id','Q01','Q02','Performed By User Code','Amb Count',
            'Action Seq','Max Action Seq','Last Amb','Fulfillment Field','Contact Method','Aspect_Combined_Roster.Center',
            'Aspect_Combined_Roster.Supervisor','Aspect_Combined_Roster.Employer','Aspect_Combined_Roster.Agent Name',
            'Yes','No','Date.Week','Date.Period_1','Ambassador','Total Surveys'],

        "drop_columns" : [
            'Contact Method'
        ],

        "headers":[
            'response_date','line_of_business','case_id','question_one','question_two','user_code','amb_count','action_seq',
            'max_action_seq','last_amb','fulfillment_field','center','supervisor','employer','agent_name','yes','no',
            'week','cient_period','ambassador','total_surveys'
        ],

        "keys":[
            'response_date','ambassador']
        }

quality = {

        "expected_columns" : [ 
            'User ID','Agent Name','Coach','Evaluation Date','Score','Calendar Week','Period','SUP','Site','LOB','Agent Tenure',
            '0-30','31-60','61-90','91-120','121-180','181-360','>360','Status'
            ],

        "team_expected_columns" : [ 
            'UserID','Employee Name','SBU','Site','SUP','Hire Date'
        ],
            
        "headers" : [
            'user_id','agent_name','coach','evaluation_date','score','week','clients_period','sup','site','lob','agent_tenure'
        ],
        
        "team_headers" : [
            'user_id','employee_name','sbu','site','sup','hire_date'
        ],

        "drop_columns" : [
            '0-30','31-60','61-90','91-120','121-180','181-360','>360','Status'
        ]
    }

