import src.scheduling.sch_handling_functions_lib as sch_fn_lib

configs = {
    "files":{
        "Altice SLU":{
            "file_type":"csv",
            "skiprows":1,
            "handling_function":sch_fn_lib.altice_sched_handling,
            "lob":"AlticeSLU",
            "expected_columns":["Code", "Nominal Date", "Start", "Stop", "HRM"],
            "input_time_format":"%H:%M %p",

            "time_columns":["Start", "Stop"],
            "date_columns":["date"],

            "code_remap_start":{"UBRK1":"LunchStart", 
                                "UBRK2-Lunch":"LunchStart", 
                                "UBRK2-Lunch-OT":"LunchStart", 
                                "UBRK3":"LunchStart",
                                "PBRK1-1st-Break":"Break 1 Start",
                                "PBRK3-2nd-Break":"Break 1 Start", 
                                "SHIFT":"TimeIn"},

            "code_remap_end":{"UBRK1":"LunchEnd", 
                                "UBRK2-Lunch":"LunchEnd", 
                                "UBRK2-Lunch-OT":"LunchEnd", 
                                "UBRK3":"LunchEnd",
                                "PBRK1-1st-Break":"Break 1 End",        
                                "PBRK3-2nd-Break":"Break 1 End", 
                                "SHIFT":"TimeOut"},

            "rename_columns":{"Nominal Date":"date", "HRM":"Employee ID"},
            "index_columns":["date", "Employee ID"],
            "output_columns":["Employee ID", "date", "TimeIn", "TimeOut", "LunchStart", "LunchEnd", "Break 1 Start", "Break 1 End"]
        }
    }
}