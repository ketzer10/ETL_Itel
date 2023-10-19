aht={
        "expected_columns":[
            'Date','Agent Name','ACD Calls','ACD Time','Avg ACD Time','ACW Time','Avg ACW Time','Hold Time',
            'Avg Hold Time','HT','Name','Supervisor','Week','month','tenure','Quarter','LOB','DEP'
            ],

        "drop_columns":[
            'Name','Week','month','Quarter'
            ],                                                                 
            
        "headers":[
            'date','agent_name','acd_calls','acd_time','avg_acd_time','acw_time','avg_acw_time','hold_time',
            'avg_hold_time','ht','supervisor','tenure','lob','dep'
            ],

        "keys":[
            'date','agent_name'
            ]
        }

adh={
        "expected_columns":
            ['Unnamed: 0', 'Unnamed: 1', 'Transaction Count', 'Scheduled In Queue', 'Actual In Queue', 'In Queue Variance', 
            'In Queue Variance %', 'Scheduled Out Of Queue', 'Actual Out Of Queue', 'Out Of Queue Variance', 'Out Queue Variance %', 
            'Total Scheduled', 'Total Variance', 'Total Adherence %', 'Name', 'Supervisor', 'Week', 'Month', 'Quarter', 
            'Tenure', 'LOB', 'DEP'],

        "drop_columns":[
            'Week','Month','Quarter'
            ],   

        "headers":[
            'agent_name', 'date', 'transaction_count', 'scheduled_in_queue', 'actual_in_queue', 'in_queue_variance', 
            'in_queue_variance_pct', 'scheduled_out_of_queue', 'actual_out_of_queue', 'out_of_queue_variance', 
            'out_of_queue_variance_pct', 'total_scheduled', 'total_variance', 'total_adherence_pct', 'list_name', 
            'supervisor', 'tenure', 'lob', 'dep'            
            ],

        "keys":[
            'date','agent_name'
            ]       
        }

avail={
        "expected_columns":[
            'Date','Agent Name','Avail','Break','Lunch','ACW','Default','Supervisor','Week','month','tenure','Quarter',
            'LOB','DEP'
            ],

        "drop_columns":[
           'Week','month','Quarter'
            ],                                                                 
            
        "headers":[
            'date','agent_name','avail','break_time','lunch','acw','defaulted','supervisor','tenure','lob','dep'
            ],

        "keys":[
            'date','agent_name'
            ]
        }

qa={
        "expected_columns":[
            'Evaluation Date','Agent Name','Score','Sup','Week','Month','Tenure','Quarter','LOB','DEP'
            ],

        "drop_columns":[
           'Week','Month','Quarter'
            ],                                                                 
            
        "headers":[
            'evaluation_date','agent_name','score','sup','tenure','lob','dep'
            ],

        "keys":[
            'evaluation_date','agent_name'
            ]
        }

sales = {
        "expected_columns":[
            'AgentName','AgentNumber','Supervisor','Calls','Quotes','Sales','Sales Premium','Quote to Call','Sale to Call',
            'Average Premium','Close rate'
            ],
        
        "drop_columns":[
            'Quote to Call','Sale to Call','Average Premium','Close rate'
        ],

        "headers":[
            'agent_name','agent_number','supervisor','calls','quotes','sales','sales_permium'
        ],
        "keys":[
            'agent_name','month'
            ]






}