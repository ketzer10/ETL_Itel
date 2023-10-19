hilton_productivity={

        "expected_columns" : [
                'Agent IDM','Agent Name','Active','Agent City','Agent CRO','Agent ZIP','Business Unit',
                'Captive/Partner','Country','Date','DC Title','Department','Employee Type','Full/Part Time',
                'Hire Date','Leader','Leader Title','Location','Month Name','Month Num','Premium Sales Team Member',
                'Schedule Type','Sr. Leader','Sr. Leader Title','State','Tenure','Tenure Bucket','Title','US/INTL',
                'Week Day','Week Num','Week Start Date','World Region','Year','Calls Handled','AHT','% VOC Composite',
                'ACW','Amex Transfers','Available Max','Available Time','Cancel','Diamond Transfers (Sales + Service)',
                'EHI Transfers','Goodwill','HD Transfers','Helpfulness','Helpfulness Count',
                'HGV Transfers','Hold Time','Hotel','Issue Resolution','Issue Resolution Count','Modify','Nights',
                'Paid Phone Time','Points Issued','Productive Time','Res Sales Transfers','Revenue','Rooms','Row Count',
                'RPC','Scheduled Time','Self Managed Time','Surveys / Call','Talk Time','Total BMG','Total Comp',
                'Total Points ($)','Total Refund','Unique Cases','Unique Resolutions','Value','Value Count',
                'VOC Composite Dem','VOC Composite Num','Conversion','AOV','Comp/Case','VOC Helpfulness','Goodwill %','Survey Count',
                'Enrollments','Non HH Rooms','HH Enrollment %',
                'HGV Transfers Main','HGV Calls Less Than 15 Sec','HGV Transfer %','GA Transfers','CC Transfers'
                ],

        "drop_columns" : [
                'Agent ZIP', 'Business Unit','Department', 'Leader', 'Leader Title', 'Month Name', 'Month Num',          # Columns to drop       
                'Schedule Type','State', 'US/INTL', 'Week Day', 'Week Num', 'World Region', 'Year','Captive/Partner'
                ],                                                                                                      
            
        "headers" : [
                'agent_idm', 'agent_name', 'active', 'agent_city', 'agent_cro', 'country', 'date', 'dc_title', 
                'employee_type','full_part_time', 'hire_date', 'location', 'premium_sales_team_member', 
                'sr_leader', 'sr_leader_title', 'tenure', 'tenure_bucket', 'title','week_start_date', 'calls_handled', 
                'aht','voc_composite', 'acw', 'amex_transfers', 'available_max', 'available_time', 'cancel',
                'diamond_transfers_sales_service','ehi_transfers','goodwill','hd_transfers', 'helpfulness', 
                'helpfulness_count','hgv_transfers','hold_time','hotel', 'issue_resolution', 
                'issue_resolution_count', 'modify', 'nights', 'paid_phone_time', 'points_issued','productive_time', 
                'res_sales_transfers', 'revenue', 'rooms', 'row_count', 'rpc','scheduled_time', 'self_managed_time', 
                'surveys_call','talk_time', 'total_bmg', 'total_comp', 'total_points','total_refund', 'unique_cases', 
                'unique_resolutions', 'value', 'value_count','voc_composite_dem','voc_composite_num', 'conversion', 
                'aov', 'comp_case', 'voc_helpfulness','goodwill_percent', 'survey_count',
                'enrollments', 'non_hh_rooms', 'hh_enrollment_percent', 'hgv_transfers_main',
                'hgv_calls_below_fifteen_sec', 'hgv_transfer', 'ga_transfers','cc_transfers'
                ],

        "keys" : [
                'agent_idm','date'
                ]
        }

team_alignments = {

        "expected_columns": [
                'Sine ID', 'HRM ID', 'Email Address', 'First Name', 'Last Name','Full Name', 'Site', 'Supervisor', 
                'Team ID', 'OnQ User ID', 'Status','LOB', 'Premium', 'Operations Manager', 'Skill & Site', 'Hire Date',
                'Term Date', 'Active', 'Term', 'Tenure', 'Tenure (buckets)'
                ],
        
        "headers" : [
                'sine_id','hrm_id','email_address','first_name','last_name','full_name','site','supervisor','team_id',
                'onq_user_id','status','lob','premium','operations_manager','skill_and_site','hire_date','term_date',
                'active','term','tenure','tenure_buckets'
                ],
        
        "trim_columns" : [
                'sine_id','hrm_id','email_address','first_name','last_name','full_name','site','supervisor','team_id',
                'onq_user_id','status','lob','operations_manager','skill_and_site','tenure_buckets'
                ],

        "upper_columns" : [
                'site', 'onq_user_id','tenure_buckets'
                ],

        "proper_columns" : [
                'first_name','last_name','full_name','supervisor','lob','operations_manager','skill_and_site',
                ]       
        }
