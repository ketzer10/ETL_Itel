from datetime import datetime as dt
from datetime import timedelta

# Dates used as parameters for the queries. Download the last 45 days.
now = dt.now().date()
start_date = now - timedelta(days=15)
end_date = now - timedelta(days=1)

configs = {
	"liveperson_agent_prod":{
		"destination_schema": "liveperson",
		"destination_table": "geo_agent_productivity",
		"params": [start_date, end_date],
		"query": """
			SELECT date,
			agent_name,
			agent_id,
			agent_email,
			interval,
			status,
			status_desc,
			skill,
			online as online_sec,
			away as away_sec,
			login_time as login_sec
			FROM liveperson.agent_prod
			WHERE date between ? and ?			
		"""
	},
	"liveperson_glb_medallia":{
		"destination_schema": "liveperson",
		"destination_table": "glb_medallia",
		"params": [start_date, end_date],
		"query": """
			SELECT customer_name,
			rep_name,
			cc_rep_internal_id,
			contact_method,
			contact_reason,
			likelihood_to_recommend,
			overall_satisfaction,
			ease_of_getting_help,
			knowledgeable,
			interest_to_help,
			negative_follow_up_comment_field,
			understands_customer_needs,
			detailed_contact_reason,
			account_number,
			live_session_id,
			brand_optimum_suddenlink,
			understands_customer_needs_2,
			knowledgeable_2,
			interest_to_help_2,
			was_genuinely_interested_in_helping_you,
			resolution_confidence,
			interaction_date,
			interaction_time,
			response_thedate,
			response_time,
			promoters,
			detractors,
			passives,
			final_comment,
			site
			FROM altice.medallia
			WHERE response_thedate between ? and ?			
		"""
	},	
	"liveperson_geo_chat_data":{
		"destination_schema": "liveperson",
		"destination_table": "geo_chat_data",
		"params": [start_date, end_date],
		"query": """
			SELECT date,
			agent_name,
			agent_id,
			agent_email,
			skill,
			ccplh,
			handled_conversation,
			closed_conversation,
			agent_load,
			first_response_time_agent_assignment,
			avg_response_time_agent,
			avg_segment_duration,
			transfers_to_skill,
			transfers_to_queue,
			close_rate,
			rcr_1_hour,
			rcr_1_day,
			rcr_3_day,
			rcr_7_day,
			mcs,
			csat_unified,
			agent_responses,
			avg_customer_responses,
			agent_segments,
			consumer_responses,
			interactive_conversations
			FROM liveperson.chat_data_new
			WHERE date between ? and ?			
		"""
	},	
	"reverse_liveperson_agent_prod":{
		"destination_schema": "liveperson",
		"destination_table": "agent_prod",
		"params": [start_date, end_date],
		"query": """
			SELECT date,
				agent_name,
				agent_id,
				agent_email,
				interval,
				status,
				status_desc,
				skill,
				online_sec as online,
				away_sec as away,
				login_sec as login_time
			FROM liveperson.geo_agent_productivity
			WHERE date BETWEEN ? AND ?		
		"""
	},	
	"reverse_liveperson_geo_chat_data":{
		"destination_schema": "liveperson",
		"destination_table": "chat_data_new",
		"params": [start_date, end_date],
		"query": """
			SELECT date,
			agent_name,
			agent_id,
			agent_email,
			skill,
			ccplh,
			handled_conversation,
			closed_conversation,
			agent_load,
			first_response_time_agent_assignment,
			avg_response_time_agent,
			avg_segment_duration,
			transfers_to_skill,
			transfers_to_queue,
			close_rate,
			rcr_1_hour,
			rcr_1_day,
			rcr_3_day,
			rcr_7_day,
			mcs,
			csat_unified,
			agent_responses,
			avg_customer_responses,
			agent_segments,
			consumer_responses,
			interactive_conversations
			FROM liveperson.geo_chat_data
			WHERE date between ? and ?			
		"""
	},	
}    