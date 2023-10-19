from datetime import datetime as dt
from datetime import timedelta

# Dates used as parameters for the queries. Download the last 45 days.
now = dt.now().date()
start_date = now - timedelta(days=30)
end_date = now - timedelta(days=1)
future_date = now + timedelta(days=15) 

configs = {
	"hrm_attendance":{
		"destination_schema": "hrm",
		"destination_table": "attendance",
		"params": [start_date, end_date, start_date, end_date],
		"query": """
			-- Get the attendance duration in seconds and only for those persons that have confirmed hours
			-- The TOP 100 PERCENT and the order by are used to speed up the SELECT DISTINCT on the roster
			WITH tmp_converted_attendance AS (
				SELECT TOP 100 PERCENT Recordid as attendance_record_id,
					Userid as user_id,
					Date as date,
					CASE
						WHEN ConfirmedOut < ConfirmedIn THEN DATEDIFF(second, ConfirmedIn, DATEADD(DAY, 1, ConfirmedOut))
						ELSE DATEDIFF(second, ConfirmedIn, ConfirmedOut)
					END AS shift_sec
				FROM dbo.tblAttendance
				WHERE ConfirmedIn IS NOT NULL AND ConfirmedOut IS NOT NULL AND Date >= ? and Date <= ?
				ORDER BY Userid DESC, Date DESC),

			-- Select only one schedule in case there are multiple. The one with the greatest approved dated
			-- The TOP 100 PERCENT and the order by are used to speed up the SELECT DISTINCT on the roster
			tmp_unique_schedules AS (
				SELECT TOP 100 PERCENT A.Userid as user_id,
					A.ScheduleDate as date,
					A.Workdayid as workday_id,
					A.timeandhalfschedule AS time_half_schedule,
					A.doubletimeschedule AS double_schedule,
					A.ShiftName as shift_name,
					A.ShiftStart AS shift_start,
					A.ShiftEnd AS shift_end
				FROM dbo.tblUserSchedules AS A
				LEFT OUTER JOIN dbo.tblUserSchedules AS B
				ON A.ScheduleDate = B.ScheduleDate AND A.Userid = B.Userid AND
				A.DateAdded < B.DateAdded
				WHERE B.Userid IS NULL AND A.ScheduleDate >= ? AND A.ScheduleDate <= ?
				ORDER BY A.Userid DESC, A.ScheduleDate DESC),

			-- Get a list of agents and dates in the schedule
			tmp_scheduled_agents AS (
				SELECT DISTINCT 
				date,
				user_id
				FROM tmp_unique_schedules),

			-- Get a list of agents and dates in which hours were worked
			tmp_present_agents AS (
				SELECT DISTINCT 
				date,
				user_id
				FROM tmp_converted_attendance),

			-- Get a roster of dates and user IDs
			tmp_dated_roster_prelim AS (
				SELECT * FROM tmp_scheduled_agents
				UNION
				SELECT * FROM tmp_present_agents),

			-- Add the department, rate, currency, and employee title ID to the roster
			tmp_dated_roster AS (
				SELECT A.user_id,
				A.date AS date,
				B.Departmentid AS department_id,
				B.Jobtitleid AS job_title_id,
				B.HourlyRate AS hourly_rate,
				B.RateCurrency AS rate_currency
				FROM tmp_dated_roster_prelim AS A
				LEFT JOIN dbo.tblEmployeeData AS B ON A.user_id = B.Userid
			),

			-- Categorize attendance details into either unapproved time or aux time
			tmp_pre_categorized_attendance_details AS (
				SELECT t2.Attendanceid                                                                                              as attendance_record_id,
				SUM(IIF(t3.RequireApproval = 1 AND t3.Paid = 1 AND t2.Approved = 0, datediff(SECOND, t2.starttime, t2.endtime), 0)) AS unapproved_sec,
				SUM(IIF(t3.RequireApproval = 0 AND t3.Paid = 0, datediff(SECOND, t2.starttime, t2.endtime), 0)) AS aux_sec
				FROM tblAttendanceDetails AS t2
				LEFT JOIN  tblAttendanceCodes AS t3 on t2.Codeid = t3.Recordid
				GROUP BY t2.Attendanceid),

			-- Convert the negative auxiliary codes into 0
			tmp_categorized_attendance_details AS (
				SELECT attendance_record_id,
					IIF(unapproved_sec < 0, 0, unapproved_sec) AS unapproved_sec,
					IIF(aux_sec < 0, 0, aux_sec) AS aux_sec
				FROM tmp_pre_categorized_attendance_details),

			-- Join the attendance and attendance details temp tables
			tmp_joined_attendance AS (
				SELECT A.user_id, 
				A.date, 
				SUM(A.shift_sec) AS shift_sec, 
				SUM(B.unapproved_sec) AS unapproved_sec, 
				SUM(B.aux_sec) AS aux_sec 
				FROM tmp_converted_attendance AS A 
				LEFT JOIN tmp_categorized_attendance_details AS B ON A.attendance_record_id = B.attendance_record_id
				GROUP BY A.user_id, A.date),

			-- Join the attendance and schedules with the dated roster
			tmp_final_attendance_schedule_data AS (
				SELECT A.date AS date,
				A.user_id AS user_id,
				A.department_id AS department_id,
				A.job_title_id AS job_title_id,
				A.hourly_rate AS hourly_rate,
				A.rate_currency AS rate_currency,
				D.BaseMultiplier AS holiday_multiplier,
				COALESCE(B.shift_sec, 0) AS shift_sec,
				COALESCE(B.unapproved_sec, 0) AS unapproved_sec,
				COALESCE(B.aux_sec, 0) AS aux_sec,
				COALESCE(B.shift_sec, 0) - COALESCE(B.unapproved_sec, 0) - COALESCE(B.aux_sec, 0) as pay_sec,
				C.workday_id AS workday_id,
				C.time_half_schedule AS time_half_schedule,
				C.double_schedule AS double_schedule,
				C.shift_name,
				C.shift_start,
				C.shift_end
				FROM tmp_dated_roster AS A
				LEFT JOIN tmp_joined_attendance AS B ON A.user_id = B.user_id AND A.date = B.date
				LEFT JOIN tmp_unique_schedules AS C ON A.user_id = C.user_id AND A.date = C.date
				LEFT JOIN dbo.tblHolidayData AS D ON A.date = CAST(D.HolidayDate AS DATE) AND (A.department_id = D.BoundDepartment OR D.BoundDepartment IS NULL)
				),

			-- Perform the time categorizations. That is, if time is time and a half, double, sick, vacation, etc
			tmp_categorized_paytime AS (
				SELECT date,
				user_id,
				department_id,
				job_title_id,
				hourly_rate,
				rate_currency,
				workday_id,
				shift_start,
				shift_end,
				shift_name,
				pay_sec,
				CASE
					WHEN shift_name like '%training%' THEN 1 else 0 END AS is_training,
				CASE
					-- Categorize the days. The order of the statement is really important. The logic behind the ordering is in the employees interest.
					-- This assumes that certain days have more benefits than others. For example: holiday, vacation, and sick can mean that the employee
					-- has payable hours even if no hours were worked.
					WHEN workday_id = 5 THEN 'Sick'
					WHEN holiday_multiplier IS NOT NULL OR workday_id = 17 THEN 'Holiday'
					WHEN workday_id = 2 THEN 'Vacation'
					WHEN time_half_schedule = 1 THEN '1.5x Schedule'
					WHEN double_schedule = 1 THEN '2.0x Schedule'
					ELSE 'Regular' END AS day_category
				FROM tmp_final_attendance_schedule_data),

			-- Split the paytime into different categories
			tmp_split_paytime AS (
				SELECT *,
				CASE
					WHEN day_category = 'Regular' AND pay_sec > 0 THEN pay_sec -- Regular work
					WHEN day_category = 'Vacation' AND pay_sec > 0 THEN pay_sec -- Scheduled for vacation but went to work
					WHEN day_category = 'Sick' AND pay_sec > 0 THEN pay_sec -- Sick day but worked at least half a day. Rest is paid as sick
					WHEN day_category = 'Regular' AND pay_sec <= 0 AND workday_id IN (6, 10) THEN 28800 -- Maternity and paid leave
					ELSE 0
				END AS base_sec,
				CASE
					WHEN day_category = '1.5x Schedule' AND pay_sec > 0 THEN pay_sec -- Regular work on a 1.5x schedule
					WHEN day_category = '1.5x Schedule' AND pay_sec <= 0 AND workday_id IN (6, 10) THEN 28800 -- Maternity and paid leave
					ELSE 0 
				END AS time_half_sec,
				CASE
					WHEN day_category = '2.0x Schedule' AND pay_sec > 0 THEN pay_sec -- Regular work on a 2.0x schedule
					WHEN day_category = '2.0x Schedule' AND pay_sec <= 0 AND workday_id IN (6, 10) THEN 28800 -- Maternity and paid leave
					ELSE 0 
				END AS double_sec,
				CASE
					WHEN day_category = 'Holiday' AND pay_sec > 0 THEN pay_sec -- Worked on a holiday
					WHEN day_category = 'Holiday' AND pay_sec <= 0 AND workday_id = 1 THEN 0 -- Scheduled but absent on a holiday
					WHEN day_category = 'Holiday' AND pay_sec <= 0 AND workday_id = 17 THEN 28800 -- Scheduled on holiday and workday id is holiday also
					ELSE 0
				END AS holiday_sec,
				CASE
					WHEN day_category = 'Vacation' AND pay_sec <= 0 THEN 28800 -- Scheduled as vacation
					ELSE 0
				END AS vacation_sec,
				CASE
					WHEN day_category = 'Sick' AND pay_sec > 0 AND pay_sec < 28800 THEN 28800 - pay_sec -- Worked at least half a day on a sick day
					WHEN day_category = 'Sick' AND pay_sec <= 0 THEN 28800 -- Did not work on a sick day
					ELSE 0	
				END AS sick_sec
				FROM tmp_categorized_paytime),
			-- If some of the columns are above 8 hours also add them to the time and a half thing
			tmp_ot_calc AS (
				SELECT A.date,
					A.user_id,
					A.department_id,
					A.job_title_id,
					A.hourly_rate,
					A.rate_currency,
					A.workday_id,
					A.shift_name,
					A.is_training,
					A.day_category,
					A.shift_start,
					A.shift_end,
					IIF(A.base_sec > 28880, 28800, A.base_sec) AS base_sec,
					IIF(A.base_sec+A.sick_sec+A.vacation_sec>28880,
						A.time_half_sec+(A.base_sec+A.sick_sec+A.vacation_sec-28800),
						A.time_half_sec) AS time_half_sec,
					A.double_sec,
					A.holiday_sec,
					IIF(A.sick_sec > 28880, 28800, A.sick_sec) AS sick_sec,
					IIF(A.vacation_sec > 28880, 28800, A.vacation_sec) AS vacation_sec,
					A.base_sec + A.time_half_sec + A.double_sec + A.holiday_sec + A.sick_sec + A.vacation_sec AS total_sec
				FROM tmp_split_paytime AS A
			)
			SELECT * FROM tmp_ot_calc AS A
			WHERE A.total_sec < 1000000

		"""
	},
	"hrm_employees":{
		"destination_schema": "hrm",
		"destination_table": "employees",
		"params": None,
		"query": """
			SELECT A.Userid AS user_id,
			A.EmployeeID AS hrm_id,
			D.FirstName AS first_name,
			D.MiddleName AS middle_name,
			D.LastName AS last_name,
			D.Gender AS gender,
			D.city AS city,
			A.Active AS is_active,
			A.HireDate AS hired_date,
			A.Jobtitleid AS job_title_id,
			C.JobTitle AS job_title,
			C.Rate AS job_standard_rate,
			A.Departmentid AS department_id,
			B.DepartmentName AS department_name,
			B.DepartmentCode AS department_code,
			A.HourlyRate AS hourly_rate,
			A.RateCurrency AS rate_currency,
			E.TermType AS termination_type,
			E.TerminationReason AS termination_reason,
			E.EffectiveDate AS termination_date,
			E.EligibleForRehire AS rehire_eligible,
			CONVERT(date, D.DateOfBirth) as date_birth,
			D.StreetAddress AS employee_address,
			CONVERT(date, D.dateadded) as date_added
		FROM dbo.tblEmployeeData AS A
		LEFT JOIN dbo.tblDepartments AS B ON B.Departmentid = A.Departmentid
		LEFT JOIN dbo.tblJobDescriptions AS C ON C.jobid = A.Jobtitleid
		LEFT JOIN dbo.tblBaseUser AS D ON D.Userid = A.Userid
		LEFT JOIN dbo.tblTerminationDetails AS E ON E.Userid = A.Userid
		"""
	},
	"hrm_departments":{
		"destination_schema": "hrm",
		"destination_table": "departments",
		"params": None,
		"query": """
			SELECT Departmentid as department_id,
				DepartmentName as department_name,
				DepartmentCode as department_code,
				Manager as manager,
				Description as description,
				Companyid as company_id,
				Internal as is_internal,
				Site as site_id,
				Active as is_active
			FROM dbo.tblDepartments
		"""
	},
	"hrm_jobs":{
		"destination_schema": "hrm",
		"destination_table": "jobs",
		"params": None,
		"query": """
			SELECT jobid as job_id,
				JobTitle as job_title,
				JobDescription as job_description,
				Rate as rate_jmd,
				Salaried as is_salaried,
				departmentid as department_id
			FROM dbo.tblJobDescriptions
		"""
	},
	"hrm_schedule_day_types":{
		"destination_schema": "hrm",
		"destination_table": "schedule_day_types",
		"params": None,
		"query": """
			SELECT Recordid as day_type_id, 
					DayType as day_type_name, 
					Paid as is_paid
				FROM dbo.tblWorkDayType
		"""
	},
	"hrm_attendance_details":{
		"destination_schema": "hrm",
		"destination_table": "attendance_details",
		"params": [start_date, end_date],
		"query": """
			SELECT A.Recordid AS record_id,
				   A.Date AS date,
				   A.Userid AS user_id,
				   A.Departmentid AS department_id,
				   CONVERT(datetime, A.StartTime) AS start_time,
				   CONVERT(datetime, A.EndTime) AS end_time,
				   A.FullStartTime AS full_start_time,
				   A.FullEndTime AS full_end_time,
				   A.Codeid AS code_id,
				   A.Approved AS is_approved,
				   A.Comment AS comment,
				   A.Approver AS approver,
				   A.ApproversComment AS approvers_comment,
				   A.UpdateComment AS update_comment
			FROM dbo.tblAttendanceDetails AS A
			WHERE A.Date >= ? AND A.Date <= ?
		"""
	},
	"hrm_attendance_codes":{
		"destination_schema": "hrm",
		"destination_table": "attendance_codes",
		"params": None,
		"query": """
			SELECT A.Recordid AS code_id,
				   A.CodeName AS code_name,
				   A.RequireApproval AS requires_approval,
				   A.PhoneCode AS phone_code,
				   A.PausedState AS paused_state,
				   A.DefaultState AS default_state,
				   A.Paid AS is_paid,
				   A.SystemIssues AS is_system_issue,
				   A.Billable AS is_billable
			FROM dbo.tblAttendanceCodes AS A
		"""
	},
	"hrm_attendance_summary":{
		"destination_schema": "hrm",
		"destination_table": "attendance_summary",
		"params": [start_date, end_date],
		"query": """
			SELECT A.Recordid as record_id,
                   A.Date AS date,
                   CONVERT(NVARCHAR(448), A.Userid) AS user_id,
                   A.Departmentid AS department_id,
                   A.SystemIn AS system_in,
                   A.SystemOut AS system_out,
                   A.ConfirmedIn AS confirmed_in,
                   A.ConfirmedOut AS confirmed_out,
                   CONVERT(NVARCHAR(448), A.Confirmer) AS confirmer,
				   A.ConfirmedTime AS confirmed_time
            FROM dbo.tblAttendance AS A
            WHERE A.Date >= ? AND A.Date <= ?
		"""
	},
	"hrm_schedules":{
		"destination_schema": "hrm",
		"destination_table": "schedules",
		"params": [start_date, future_date],
		"query": """
			SELECT A.Scheduleid AS schedule_id,
				   A.ScheduleDate AS schedule_date,
				   A.Departmentid AS department_id,
				   A.Userid AS user_id,
				   A.Workdayid AS workday_id,
				   A.Scheduler AS scheduler,
				   A.Shiftid AS shift_id,
				   A.ShiftStart AS shift_start,
				   A.ShiftEnd AS shift_end,
				   CONVERT(datetime, A.Break1Start) AS break_one_start,
				   CONVERT(datetime, A.Break1End) AS break_one_end,
				   CONVERT(datetime, A.Break2Start) AS break_two_start,
				   CONVERT(datetime, A.Break2End) AS break_two_end,
				   CONVERT(datetime, A.LunchStart) AS lunch_start,
				   CONVERT(datetime, A.LunchEnd) AS lunch_end,
				   A.ShiftName AS shift_name,
				   A.TimeAndHalfSchedule AS time_half_schedule,
				   A.DoubleTimeSchedule AS double_time_schedule,
				   CONVERT(date, A.DateAdded) as date_added
			FROM dbo.tblUserSchedules AS A
			WHERE A.ScheduleDate >= ? AND A.ScheduleDate <= ?
		"""
	}
}