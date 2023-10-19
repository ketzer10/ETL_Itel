from datetime import datetime as dt
from datetime import timedelta

# Dates used as parameters for the queries. Download the last 45 days.
now = dt.now().date()
start_date = now - timedelta(days=45)
end_date = now - timedelta(days=1)

configs = {
	"employees":{
		"destination_schema": "hrmaster",
		"destination_table": "employees",
		"params": None,
		"query": """
			SELECT employee_id::text AS legacy_id,
			first_name,
			last_name,
			date_birth,
			national_id_number,
			hired_date,
			separation_date,
			national_id_document,
			status,
			direct_report_id,
			direct_report_name,
			hiring_comments,
			employment_scheme,
			contract_signed,
			added_payroll,
			is_remote,
			personal_email,
			work_email,
			address,
			phone_number,
			nis,
			nis_name,
			tin,
			number_kids,
			badge_type,
			lob_id,
			client_id,
			lob_name,
			client_name,
			contract_status,
			country,
			title_id,
			title_name,
			department_id,
			department_name,
			gender,
			language,
			wave,
			tenure_days,
			insurance_premium,
			insurance_effective_date,
			insurance_policy_number,
			insurance_coverage,
			insurance_status,
			full_name
		FROM hrmaster.hr_employee_database
		"""
	},
	"attrition":{
		"destination_schema": "hrmaster",
		"destination_table": "attrition",
		"params": None,
		"query": """
			SELECT emerge_id::text as legacy_id,
			full_name,
			first_name,
			last_name,
			status,
			client,
			line_business,
			employee_title,
			direct_report,
			hired_date,
			notice_date,
			separation_date,
			date_birth,
			wave,
			country,
			separation_type,
			separation_reason,
			separation_phase,
			breached_kpi,
			comments,
			is_rehireable,
			certified_by,
			client_portal_termination,
			completed_exit_interview,
			department_name,
			gender
		FROM hrmaster.hr_attrition
		"""
	}
}