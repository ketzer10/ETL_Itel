sheets_configs = {
    "active_dump": {
        "sheet_name": "Active Dump",
        "use_cols": [
            "Last, First", "LOCATION", "Supervisor", "NORM EID",
            "DDP ID", "LCP EXT", "EmailAddress",
            "NetworkID", "Hire Date", "Term Date",
            "Batch #", "Ewfm ID", "WFH/WFS",
            "Verient ID", "HRM ID", "LOB"
            ],
        "to_rename_cols": {
            'Last, First': 'agent_name',
            'LOCATION': 'location',
            'Supervisor': 'supervisor_name',
            'NORM EID': 'norm_eid',
            'DDP ID': 'ddp_id',
            'LCP EXT': 'lcp_ext',
            'EmailAddress': 'emailaddress',
            'NetworkID': 'networkid',
            'Hire Date': 'hire_date',
            'Term Date': 'term_date',
            'Batch #': 'batch_no',
            'Ewfm ID': 'ewfm_id',
            'WFH/WFS': 'wfh_wfs',
            'Verient ID': 'verient_id',
            'HRM ID': 'hrm_id',
            'LOB': 'lob'
            },
        #"int_cols": ["Verient ID", "HRM ID"],
        "date_cols": ["Hire Date", "Term Date"],
        "read_dtypes": {
            "LCP EXT": str,
            "Verient ID": str,
            "HRM ID": str
            },
        "name_cols": ["Last, First", "Supervisor"],
        "to_add_columns": ["term_date"]
        },
    
    "temination_dump": {
        "sheet_name": "Termination Dump",
        "use_cols": ["Last, First", "LOCATION", "Internal Supervisor",
                     "NORM EID", "DDP ID", "EmailAddress",
                     "NetworkID", "Hire Date", "Term Date",
                     "Batch #", "WFS/WFH", "Verient ID",
                     "HRM ID", "LOB"],
        "to_rename_cols": {
            'Last, First': 'agent_name',
            'LOCATION': 'location',
            'Internal Supervisor': 'supervisor_name',
            'NORM EID': 'norm_eid',
            'DDP ID': 'ddp_id',
            'EmailAddress': 'emailaddress',
            'NetworkID': 'networkid',
            'Hire Date': 'hire_date',
            "Term Date": "term_date",
            'Batch #': 'batch_no',
            'WFS/WFH': 'wfh_wfs',
            'Verient ID': 'verient_id',
            'HRM ID': 'hrm_id',
            'LOB': 'lob'
            },
        #"int_cols": ["Verient ID", "HRM ID"],
        "date_cols": ["Hire Date", "Term Date"],
        "read_dtypes": {
            "Verient ID": str,
            "HRM ID": str
            },
        "name_cols": ["Last, First", "Internal Supervisor"],
        "to_add_columns": ["ewfm_id", "lcp_ext"]
    }
}

final_cols = [
    'agent_name', 'supervisor_name', 'norm_eid', 'ddp_id',
    'emailaddress', 'networkid', 'hire_date', 'batch_no', 'term_date',
    'wfh_wfs', 'verient_id', 'hrm_id', 'lob', 'ewfm_id', 'lcp_ext', 'location']