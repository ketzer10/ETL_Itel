from datetime import datetime as dt
from datetime import timedelta

# Dates used as parameters for the queries. Download the last 45 days.
now = dt.now().date()
start_date = now - timedelta(days=15)
end_date = now - timedelta(days=1)

configs = {
	"od_geo_agent_activity_team_time":{
		"destination_schema": "office_depot",
		"destination_table": "geo_agent_activity_team_time",
		"params": [start_date, end_date],
		"query": """
            SELECT office_depot_id::text,
            agent_name,
            thedate,
            team_name,
            staff_hours,
            total_time,
            call_count,
            idle_time,
            idle_lunch,
            idle_break,
            acw_hours,
            idle_coach,
            idle_train,
            idle_meeting,
            idle_spec,
            idle_obp,
            idle_other,
            available_time,
            hold_count,
            hold_time,
            handle_time,
            wrap_time,
            ring_time,
            not_resp_time
            FROM office_depot.agent_activity_by_team_and_time
            WHERE thedate between ? and ?			
		"""
	},
	"od_wah_agent_activity_team_time":{
		"destination_schema": "office_depot",
		"destination_table": "wah_agent_activity_team_time",
		"params": [start_date, end_date],
		"query": """
            SELECT office_depot_id::text,
            agent_name,
            thedate,
            team_name,
            staff_hours,
            total_time,
            call_count,
            idle_time,
            idle_lunch,
            idle_break,
            acw_hours,
            idle_coach,
            idle_train,
            idle_meeting,
            idle_spec,
            idle_obp,
            idle_other,
            available_time,
            hold_count,
            hold_time,
            handle_time,
            wrap_time,
            ring_time,
            not_resp_time
            FROM office_depot.agent_activity_by_team_and_time_wah
		WHERE thedate between ? and ?
		"""
	},
	"od_geo_journey_agent_summary":{
		"destination_schema": "office_depot",
		"destination_table": "geo_journey_agent_summary",
		"params": [start_date, end_date],
		"query": """
            SELECT agent_id,
            thedate as date,
            staff_sec,
            initial_login_time,
            final_logout_time,
            total_available_time_sec,
            total_inbound_talk_time_sec,
            total_inbound_hold_time_sec,
            total_inbound_connected_time_sec,
            total_outdial_talk_time_sec,
            total_outdial_hold_time_sec,
            total_outdial_connected_time_sec,
            total_inbound_wrap_up_time_sec,
            total_outdial_wrap_up_time_sec,
            calls_handled
            FROM office_depot.journey_agent_summary_bpo
            WHERE thedate between ? and ?            
		"""
	},
	"od_wah_journey_agent_summary":{
		"destination_schema": "office_depot",
		"destination_table": "wah_journey_agent_summary",
		"params": [start_date, end_date],
		"query": """
            SELECT agent_id,
            thedate as date,
            staff_sec,
            initial_login_time,
            final_logout_time,
            total_available_time_sec,
            total_inbound_talk_time_sec,
            total_inbound_hold_time_sec,
            total_inbound_connected_time_sec,
            total_outdial_talk_time_sec,
            total_outdial_hold_time_sec,
            total_outdial_connected_time_sec,
            total_inbound_wrap_up_time_sec,
            total_outdial_wrap_up_time_sec,
            calls_handled
            FROM office_depot.journey_agent_summary_wah
            WHERE thedate between ? and ?            
		"""
	},
	"od_glb_journey_calls_handled_by_queue_team":{
		"destination_schema": "office_depot",
		"destination_table": "glb_calls_handled_queue_team",
		"params": [start_date, end_date],
		"query": """
            SELECT queue,
            site,
            team,
            thedate,
            completed,
            disconnected,
            transferred,
            transferred_out,
            blind_transfers,
            requeued,
            answered,
            secondary_answered,
            consult_count,
            ctq_request_count,
            conference_count,
            hold_count
            FROM office_depot.calls_handle_by_queue_team
            WHERE thedate between ? AND ?         
		"""
	},
	"od_geo_crm_daily_chat_phone": {
		"destination_schema": "office_depot",
		"destination_table": "geo_crm_daily_chat_phone",
		"params": [start_date, end_date],
		"query": """
            SELECT
                  thedate as date,
                  thename as agent_name,
                  office_depot_id,
                  aops_id,
                  reference,
                  connect_text,
                  resolve_text,
                  ease_text,
                  ltr,
                  queue_name,
                  connect_score,
                  resolve_score,
                  ease_score,
                  promoters,
                  detractors,
                  passives
            FROM office_depot.crm_daily_chat_phone   
		WHERE thedate between ? AND ?; 
            """
	},
	"od_wah_crm_daily_phone": {
		"destination_schema": "office_depot",
		"destination_table": "wah_crm_daily_phone",
		"params": [start_date, end_date],
		"query": """
            SELECT
                  thedate as date,
                  thename as agent_name,
                  office_depot_id,
                  aops_id,
                  reference,
                  connect_text,
                  resolve_text,
                  ease_text,
                  ltr,
                  queue_name,
                  connect_score,
                  resolve_score,
                  ease_score,
                  promoters,
                  detractors,
                  passives
            FROM office_depot.crm_daily_phone_wah   
		WHERE thedate between ? AND ?;
            """ 
	},    
      "od_geo_chat_activity_oracle": {
		"destination_schema": "office_depot",
		"destination_table": "geo_chat_activity_oracle",
		"params": [start_date, end_date],
		"query": """
            SELECT
                  thedate as date,
                  agent_name,
                  login_time as login_time_sec,
                  logins,
                  chats,
                  chats_logins,
                  engaged_time_percent,
                  transfer_out,
                  transfer_in,
                  declined_transfers,
                  conf_total,
                  dec_conf_total
            FROM office_depot.chat_activity_bpo_oracle
		WHERE thedate between ? AND ?; 
            """
	},    
      "od_geo_agent_activity_by_channel": {
		"destination_schema": "office_depot",
		"destination_table": "geo_agent_activity_by_channel",
		"params": [start_date, end_date],
		"query": """
            SELECT
                  office_depot_id,
                  login_id,
                  team_name,
                  thedate as date,
                  calls,
                  aht,
                  cpwh,
                  long_calls_ct,
                  short_calls_ct,
                  blind_xfer_ct,
                  xfer_ct,
                  hold_ct,
                  agent_terminated_ct,
                  first_activity,
                  last_activity
            FROM office_depot.agent_activity_by_channel
            WHERE thedate between ? AND ?;
            """
	},    
      "od_wah_agent_activity_by_channel": {
		"destination_schema": "office_depot",
		"destination_table": "wah_agent_activity_by_channel",
		"params": [start_date, end_date],
		"query": """
            SELECT
                  office_depot_id,
                  login_id,
                  team_name,
                  thedate as date,
                  calls,
                  aht,
                  cpwh,
                  long_calls_ct,
                  short_calls_ct,
                  blind_xfer_ct,
                  xfer_ct,
                  hold_ct,
                  agent_terminated_ct,
                  first_activity,
                  last_activity
            FROM office_depot.agent_activity_by_channel_wah
            WHERE thedate between ? AND ?;		
            """
	},
      "od_internal_qa": {
		"destination_schema": "office_depot",
		"destination_table": "geo_customer_service",
		"params": [start_date, end_date],
		"query": """
            SELECT sitename as sitename,
                  thedate as date,
                  sessionid,
                  lob,
                  thename as agent_name,
                  office_depot_id,
                  final_score,
                  pointsearnedconnection AS points_earned_connect,
                  pointsearnedease AS points_earned_easy,
                  pointsearnedresolution AS points_earned_resolution,
                  pointspossibleconnection AS points_possible_connect,
                  pointspossibleease AS points_possible_easy,
                  pointspossibleresolution AS points_possible_resolution,
                  reviewer
            FROM office_depot.internal_qa
            """
	},
      "od_reverse_calls_handled": {
		"destination_schema": "office_depot",
		"destination_table": "calls_handle_by_queue_team",
		"params": [start_date, end_date],
		"query": """
            SELECT queue,
                  site,
                  team,
                  thedate,
                  completed,
                  disconnected,
                  transferred,
                  transferred_out,
                  blind_transfers,
                  requeued,
                  answered,
                  secondary_answered,
                  consult_count,
                  ctq_request_count,
                  conference_count,
                  hold_count
            FROM office_depot.glb_calls_handled_queue_team
            WHERE thedate between ? and ?
            """
	},
	"od_reverse_team_time":{
		"destination_schema": "office_depot",
		"destination_table": "agent_activity_by_team_and_time",
		"params": [start_date, end_date],
		"query": """
            SELECT office_depot_id,
            agent_name,
            thedate,
            team_name,
            staff_hours,
            total_time,
            call_count,
            idle_time,
            idle_lunch,
            idle_break,
            acw_hours,
            idle_coach,
            idle_train,
            idle_meeting,
            idle_spec,
            idle_obp,
            idle_other,
            available_time,
            hold_count,
            hold_time,
            handle_time,
            wrap_time,
            ring_time,
            not_resp_time
            FROM office_depot.geo_agent_activity_team_time
            WHERE thedate between ? and ?			
		"""
	}               
}    