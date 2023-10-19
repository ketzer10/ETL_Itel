glb_csat = {

    "selected_columns": [
            'Custom Employee Id','Name','Requests','Responses','Percent Positive','vs prev 1 days','Percent Negative',
            'vs prev 1 days','Percent Resolved','vs prev 1 days','Total','Clarity','Friendliness','Knowledge','Problem Solving',
            'Professionalism','Responsiveness','Total','Above and beyond','Focus on my needs','Friendly','Knowledgeable',
            'Patient',  'Speedy','Reviews','Avg. Score'
    ],

    "drop_columns": [
            'Email','Partner - Digital QA Form'
    ],

    "headers": [
            'custom_employee_id','name','requests','responses','percent_positive','vs_prev_one_days_positive','percent_negative','vs_prev_one_days_negative',
            'percent_resolved','vs_prev_one_days_resolved','imp_total','imp_clarity','imp_friendliness','imp_knowledge','imp_problem_solving',
            'imp_professionalism','imp_responsiveness','exc_total','exc_above_and_beyond','exc_focus_on_my_needs','exc_friendly','exc_knowledgeable',
            'exc_patient','exc_speedy','qa_reviews','qa_avg_score','site'
    ],

    "pct_columns" : ['percent_positive','vs_prev_one_days_positive','percent_negative','vs_prev_one_days_negative',
            'percent_resolved','vs_prev_one_days_resolved','qa_avg_score'

    ],

    "keys": [
        'custom_employee_id','date'
    ]

}