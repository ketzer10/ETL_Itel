roster_configs = {
    "sheet_name": "HC Roster",
    "use_cols": [
        "BPO/WAH", "Site", "Emp. ID", "Status",
        "Position", "Full Name", "Supervisor", "Manager",
        "Connection Type", "Language", "VCCID", "WM Login",
        "Wave", "Hire Date", "NSTG Date", "Prod. Date", "Transferred To",
        "Transferred From", "Transfer Date", "Attri. Date",
    ],
    "read_dtypes": {
        "Emp. ID": str,
        "VCCID": str
    },
    "date_cols": [
        "Hire Date", "NSTG Date", "Prod. Date", "Transfer Date", "Attri. Date"
    ],
    "replace_dash": [
        "Transferred To", "Transferred From", "Transfer Date", "Attri. Date"
    ],
    "rename_cols": {
        "BPO/WAH": "bpo_wah",
        "Site": "site",
        "Emp. ID": "legacy_id",
        "Status": "status",
        "Position": "position",
        "Full Name": "full_name",
        "Supervisor": "supervisor",
        "Manager": "manager",
        "Connection Type": "connection_type",
        "Language": "language",
        "VCCID": "vccid",
        "WM Login": "wm_login",
        "Wave": "wave",
        "Hire Date": "hire_date",
        "NSTG Date": "nstg_date",
        "Prod. Date": "prod_date",
        "Transferred To": "transferred_to",
        "Transferred From": "transferred_from",
        "Transfer Date": "transfer_date",
        "Attri. Date": "attri_date"
    },
    "final_cols": [
        'legacy_id', 'vccid', 'wm_login', 'full_name', 'position',  'supervisor', 'manager',
        'bpo_wah', 'site', 'status',  'connection_type', 'language', 'wave', 'hire_date',
        'nstg_date', 'prod_date', 'transferred_to', 'transferred_from', 'transfer_date', 'attri_date'
    ]
}