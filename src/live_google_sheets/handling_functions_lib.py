import numpy as np
import utils.dfutils as dfutils

# Functions for handling worksheets of anyone medical leaves
def handling_worksheets_sap_medical_leaves(worksheets, worksheets_names):
    for i in range(len(worksheets)):
        worksheets[i][["agent_name", "legacy_id"]] = worksheets[i]["agent_name_id"].str.split( " _ ", expand = True)
        worksheets[i]["flag"] = ''
 

 # Functions for all Guyana Training Manual Trackers
def handling_grand_worksheet_guyana_training_tracker(grand_worksheet):
    grand_worksheet.columns = grand_worksheet.columns.str.lower()

    grand_worksheet["flag"] = ''    
    #grand_worksheet.index = np.arange(3, len(grand_worksheet)+3)
    #grand_worksheet.index.name = "the_index"
    grand_worksheet["the_index"] = np.arange(3, len(grand_worksheet)+3)

    grand_worksheet["agentid"] = grand_worksheet["agentid"].astype('str')
    grand_worksheet["agentid"] = grand_worksheet["agentid"].apply(lambda txt: txt.split(".")[0])    


# Functions for Honduras Manual Trackers
def handling_grand_worksheet_honduras_manual_trackers(grand_worksheet):
    grand_worksheet["flag"] = '' 
    index =  grand_worksheet[grand_worksheet["regular_hours_worked"].str.startswith('-', na=False)].index
    grand_worksheet.loc[index, "flag"] = 'Negative Hours '

    index = grand_worksheet[grand_worksheet["week_shift_type"].isna()].index
    grand_worksheet.loc[index, "flag"] = grand_worksheet.loc[index, "flag"] + f'Missing week shift type ' 

    grand_worksheet["legacy_id"] = grand_worksheet["legacy_id"].astype('str')
    grand_worksheet["legacy_id"] = grand_worksheet["legacy_id"].apply(lambda txt: txt.split(".")[0])


# Functions for Google Forms responses
def handling_worksheet_google_form_responses_timestamp(grand_worksheet):
    grand_worksheet["Timestamp"] = grand_worksheet["Timestamp"].astype('datetime64[ns]')

# Anyone Home  Mappings
def handling_grand_worksheet_anyonehome_mappings(grand_worksheet):
    grand_worksheet["aoh_id"] = grand_worksheet["aoh_id"].astype('str')
    grand_worksheet["aoh_id"] = grand_worksheet["aoh_id"].apply(lambda txt: txt.split(".")[0])

# Liveperson Mappings
def handling_grand_worksheet_liveperson_mappings(grand_worksheet):
    grand_worksheet.columns = grand_worksheet.columns.str.lower()
    grand_worksheet["liveperson_id"] = grand_worksheet["liveperson_id"].astype('str')
    grand_worksheet["liveperson_id"] = grand_worksheet["liveperson_id"].apply(lambda txt: txt.split(".")[0])
    grand_worksheet["liveengage_altice_id"] = grand_worksheet["liveengage_altice_id"].astype('str')
    grand_worksheet["liveengage_altice_id"] = grand_worksheet["liveengage_altice_id"].apply(lambda txt: txt.split(".")[0])       

# Office Depot Mappings
def handling_grand_worksheet_office_depot_mappings(grand_worksheet):
    grand_worksheet["team_time_id"] = grand_worksheet["team_time_id"].astype('str')
    grand_worksheet["team_time_id"] = grand_worksheet["team_time_id"].apply(lambda txt: txt.split(".")[0])

    grand_worksheet["office_depot_id"] = grand_worksheet["office_depot_id"].astype('str')
    grand_worksheet["office_depot_id"] = grand_worksheet["office_depot_id"].apply(lambda txt: txt.split(".")[0])

def handling_office_depot_qa(grand_worksheet):
    grand_worksheet.columns = ["timestamp", "email_address", "session_id", "qa_name_id", "q1", "q2", "q3", 
                                "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "comments", 
                                "supervisor_name_id", "lob", "employee_name_id", "score"]
    grand_worksheet['date']=grand_worksheet['timestamp'].str.split(' ',2,expand=True)[0].astype('datetime64[ns]')                # Handle the date
    
    grand_worksheet[['employee_name','employee_id']]=grand_worksheet['employee_name_id'].str.split(' _ ',2,expand=True)          # Handle the agent name and employee_id
    grand_worksheet[['supervisor','supervisor_id']]=grand_worksheet['supervisor_name_id'].str.split(' _ ',2,expand=True)         # Handle the supervisor name and employee_id
    grand_worksheet[['quality_auditor_name','quality_auditor_id']]=grand_worksheet['qa_name_id'].str.split(' _ ',2,expand=True)  # Handle the quality auditor name and employee_id

    output_columns = ["date", "email_address", "session_id", "employee_id", "employee_name", "score", "q1", "q2", 
                     "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "supervisor", 
                      "supervisor_id", "lob", "quality_auditor_id", "quality_auditor_name"]
    grand_worksheet = grand_worksheet[output_columns]

    ids = ["employee_id", "supervisor_id", "quality_auditor_id"]
    for id in ids:
        grand_worksheet[id] = grand_worksheet[id].astype('str')
        grand_worksheet[id] = grand_worksheet[id].apply(lambda txt: txt.split(".")[0])    

    grand_worksheet["score"] = grand_worksheet["score"].replace("#DIV/0!", '')

    grand_worksheet["session_id"] = grand_worksheet["session_id"].str[:254]