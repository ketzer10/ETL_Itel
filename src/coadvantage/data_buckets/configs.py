configs = {
    "employee_info": {
        "rename_cols": {
            "Employee_ID": "coad_id",
            "First Name": "first_name",
            "Middle Name": "middle_name",
            "Last Name": "last_name",
            "Job Title": "job_title",
            "Division_Desc": "division_description",
            "Gender": "gender",
            "Birth Date": "date_birth",
            "Active Ee": "status",
            "EE Terminated Date": "termination_date",
            "Last Hire Date": "hired_date",
            "Manager/Supervisor": "direct_report"
        },
        "date_cols": ["hired_date", "date_birth", "termination_date"],
        "expected_cols": ["Employee_ID", "First Name", "Middle Name", "Last Name", "Job Title", "Division_Desc", 
                          "Gender", "Birth Date", "Active Ee", "EE Terminated Date", "Last Hire Date", 
                          "Manager/Supervisor"],
        "sharepoint_config_key": "coadvantage_employee_data"
    },
    "time_sheet": {
        "rename_cols": {
            "Employee Id": "coad_id",
            "First Name": "first_name",
            "Last Name": "last_name",
            "In Time": "in_time",
            "Out Time": "out_time",
            "Regular Hours": "regular_hours",
            "Overtime Hours": "overtime_hours",
            "Shift Differential Hours": "shift_differential_hours",
            "Division(1)": "division",
            "Date": "date",
            "Total Work Hours": "total_work_hours"
        },
        "date_cols": ["date"],
        "expected_cols": ["Employee Id", "First Name", "Last Name", "Date", "In Time", "Out Time", "Total Work Hours", 
                          "Regular Hours", "Overtime Hours", "Shift Differential Hours", "Division(1)"],
        "sharepoint_config_key": "coadvantage_timesheet"
    }
}