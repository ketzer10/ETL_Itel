sheet_config = {
    "sheet_name": "All",
    "use_cols": [
        'Country', 'Site', 'Avaya 107#', 'EUID(ITE#)', 'Name', 'WFM ID',
        'HRM ID', 'Operations Manager', 'Supervisor', 'LOB Assigned',
        'B&M / WAH', 'Role', 'SD Status', '106 Number', 'CMS Name',
        'Itel Email Address', 'Kroger Email Address', 'Personal Email Address',
        'Address', 'City', 'State', 'Country.1', 'Zip', 'Contact Numbers',
        'Emergency Contact Name', 'Emergency Contact Relationship',
        'Emergency Contact Number', 'ITEL START DATE', 'Aspect Hire Date',
        'Current Day', 'Tenure_Days', 'Tenure Category', 'Attrition Date'
    ],
    "rename_cols": {
        'Country': 'country',
        'Site': 'site',
        'Avaya 107#': 'avaya_107',
        'EUID(ITE#)': 'euid_ite',
        'Name': 'name',
        'WFM ID': 'wfm_id',
        'HRM ID': 'hrm_id',
        'Operations Manager': 'operations_manager',
        'Supervisor': 'supervisor',
        'LOB Assigned': 'lob_assigned',
        'B&M / WAH': 'bm_wah',
        'Role': 'role',
        'SD Status': 'sd_status',
        '106 Number': 'number_106',
        'CMS Name': 'cms_name',
        'Itel Email Address': 'itel_email_address',
        'Kroger Email Address': 'kroger_email_address',
        'Personal Email Address': 'personal_email_address',
        'Address': 'address',
        'City': 'city',
        'State': 'state',
        'Country.1': 'country1',
        'Zip': 'zip',
        'Contact Numbers': 'contact_numbers',
        'Emergency Contact Name': 'emergency_contact_name',
        'Emergency Contact Relationship': 'emergency_contact_relationship',
        'Emergency Contact Number': 'emergency_contact_number',
        'ITEL START DATE': 'itel_start_date',
        'Aspect Hire Date': 'aspect_hire_date',
        'Current Day': 'current_day',
        'Tenure_Days': 'tenure_days',
        'Tenure Category': 'tenure_category',
        'Attrition Date': 'attrition_date'
    },
    "text_cols": [
        'country', 'site', 'avaya_107', 'euid_ite', 'name', 'wfm_id', 'hrm_id',
        'operations_manager', 'supervisor', 'lob_assigned', 'bm_wah', 'role',
        'sd_status', 'number_106', 'cms_name', 'itel_email_address',
        'kroger_email_address', 'personal_email_address', 'address', 'city',
        'state', 'country1', 'zip','contact_numbers', 'emergency_contact_name',
        'emergency_contact_relationship', 'emergency_contact_number',
        'tenure_days', 'tenure_category'
    ],
    "date_cols": [
        'itel_start_date', 'aspect_hire_date',
        'current_day', 'attrition_date'
    ]
}