requests = {
    "main_table_request":{
        "url": "https://central.anyonehome.com/CallCenter/qaReportList",
        "cookies": {
            "G_ENABLED_IDPS": "google",
            "central": "ihq0tfq1veglhh1b0bio05r7od1aa7qk",
        },
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://central.anyonehome.com",
            "Connection": "keep-alive",
            "Referer": "https://central.anyonehome.com/callcenter/view_shop_report/all",
        },
        "data": [
            ("type", "all"),
            ("accountId[]", ""),
            ("property[]", ""),
            ("agentId[]", ""),
            ("shopScoreMin", ""),
            ("shopScoreMax", ""),
            ("create_shop_category[]", "Leasing,Audit"),
            ("supervisor[]", ""),
            ("location[]", "Guyana,Honduras,Belize"),
            ("date_range", "Custom"),
            ("qa_from_date", "01/01/2019"),
            ("qa_to_date", "01/01/2030"),
            ("coach_completed_date_range", "Custom"),
            ("qa_coachc_from_date", ""),
            ("qa_coachc_to_date", ""),
            ("case_sr_created_date_range", "Custom"),
            ("qa_report_case_sr_from_date", ""),
            ("qa_report_case_sr_to_date", ""),
            ("qa_completed_date_range", "Custom"),
            ("qa_completed_from_date", "03/01/2021"),
            ("qa_completed_to_date", "03/01/2021"),
            ("buildCols[]", "Account"),
            ("buildCols[]", "Property"),
            ("buildCols[]", "Agent Name"),
            ("buildCols[]", "Supervisor"),
            ("buildCols[]", "Shop Score"),
            ("buildCols[]", "Shop Category"),
            ("buildCols[]", "Shop Created Date"),
            ("buildCols[]", "Case/Service Request Created Date"),
            ("buildCols[]", "Coaching Completed Date/TIme"),
            ("buildCols[]", "Coaching Completed"),
            ("buildCols[]", "Shop Completed Date"),
            ("all_qa_score_count", ""),
            ("isTableData", "true"),
            ("startIndex", "0"),
            ("limit", "10"),
            ("sortBy", "undefined"),
            ("sortDirection", "undefined"),
            ("search", "undefined"),]
    },
    "detail_card_request": {
        'url': 'https://central.anyonehome.com/QualityAssurance/editQaForm',
        "cookies": {
            "G_ENABLED_IDPS": "google",
            "central": "ihq0tfq1veglhh1b0bio05r7od1aa7qk",
        },
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://central.anyonehome.com",
            "Connection": "keep-alive",
            "Referer": "https://central.anyonehome.com/callcenter/view_shop_report/all",
        },
        "data": {
            "shopSfid": "662697",
            "caseStatus": "Inquiry",
            "shopCategory": "Leasing",
            "srpop": "",
            "origin": "Phone",
            "qadispute": "true"
        }
    },
    "login_request": {
        "url": "https://central.anyonehome.com/signin",
        "cookies": {
            "G_ENABLED_IDPS": "google",
        },
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://central.anyonehome.com",
            "Connection": "keep-alive",
            "Referer": "https://central.anyonehome.com/signin",
            "Upgrade-Insecure-Requests": "1",
        },
        "data": {
            "email_address": "placeholder",
            "password": "placeholder"
        }
    }
}

general_params = {
    "main_table": {
        "expected_cols": ["shop_sfid", "account", "property", "supervisor", "shopscore", "agentname",
                           "shopcreateddate", "coachingcompleteddate/time", "case/servicerequestcreateddate",
                           "shopcategory", "coaching_required", "coachingcompleted", "supervisor_coaching_completed",
                           "case_status", "download_link", "submitters_notes", "coaching_notes", "resolvers_notes",
                           "origin", "service_request_pop", "shopcompleteddate", "atfaultforpop", "total_count"],
        "rename_cols": {
            "shopscore": "shop_score",
            "agentname": "agent_name",
            "shopcategory": "shop_category",
            "shopcreateddate": "shop_created_date",
            "coachingcompleteddate/time": "coaching_completed_datetime",
            "case/servicerequestcreateddate": "case_service_request_created_date",
            "shop_category": "shop_category",
            "coachingcompleted": "coaching_completed",
            "shopcompleteddate": "shop_completed_datetime",
            "atfaultforpop": "at_fault_for_pop"},
        "datetime_cols": ["shop_created_date", "shop_completed_datetime", "case_service_request_created_date", 
                          "coaching_completed_datetime"],
        "float_cols": ["shop_score"],
        "bool_cols": ["coaching_required"],
        "drop_cols": ["total_count"]
    },
    "common": {
        "card_cols": ["shop_sfid", "qa_form_name", "qa_reviewer", "call_skill", "call_duration", "supervisor_name", "team_lead_1",
                      "team_lead_2", "grader_notes", "prospect_info_completed", "first_name", "last_name", "phone_number", 
                      "email", "professional", "call_ending", "care", "outstanding_shop"],
        "float_cols": ["call_duration"]
    },
    "maintenance": {
        "real_shop_type": "Maintenance",
        "schema": "anyone_home",
        "table_name": "glb_external_qa_maintenance",
        "card_cols": ["case_creation_datetime", "property_unit_needing_service", "room_area_impacted", 
                      "sr_type", "permission_to_enter", "entry_info", "troubleshooting", "empathy", 
                      "navigation_accuracy", "work_order_notes"],
        "datetime_cols": ["case_creation_datetime"]
    },
    "audit_leasing": {
        "real_shop_type": "Audit,Leasing",
        "schema": "anyone_home",
        "table_name": "glb_external_qa_audit_leasing",
        "card_cols": ["case_creation_datetime", "bedandbath", "pets", "reason_for_moving", "floorplan_of_interest",
                      "rent_range", "move_in", "building_value", "no_of_occupants", "attempt_showing", 
                      "qualification_policies", "engaging_rapport", "notes", "navigation", "accuracy"],
        "datetime_cols": ["case_creation_datetime"]
    }

}