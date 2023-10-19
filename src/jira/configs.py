from src.jira.jira_utils import *

configs = {
    "projects": {
		"query_data": False,
		"get_all_data_function": get_all_projects,
		"get_data_with_details_function": get_needed_details_of_all_projects,
		"columns_to_normalize": ["type_key", "style"],
		"aux_tables_names": ["projects_type_keys", "projects_styles"],
        "foreign_to_rename": {"type_key": "type_key_id", "style": "style_id"},
        "date_columns": False,
        "schema": "jira",
        "table_name": "projects"
    },
    "users": {
		"query_data": False,
		"get_all_data_function": get_all_users,
		"get_data_with_details_function": get_needed_details_of_all_users,
		"columns_to_normalize": False,
        "aux_tables_names": False,
        "date_columns": False,
		"schema": "jira",
		"table_name": "users"
    },
    "boards": {
		"query_data": "SELECT id FROM jira.projects;",
		"get_all_data_function": False,
		"get_data_with_details_function": get_needed_details_of_all_boards,
		"columns_to_normalize": ["type"],
        "aux_tables_names": ["boards_types"],
        "foreign_to_rename": {"type": "type_id"},
        "date_columns": False,
		"schema": "jira",
		"table_name": "boards"
    },
	"sprints": {
		"query_data": "SELECT id FROM jira.boards;",
		"get_all_data_function": False,
		"get_data_with_details_function": get_needed_details_of_all_sprints,
		"columns_to_normalize": ["state"],
		"aux_tables_names": ["sprints_states"],
        "foreign_to_rename": {"state": "state_id"},
        "date_columns": ["start_date", "end_date", "complete_date"],
        "schema": "jira",
        "table_name": "sprints"
	},
	"issues_sprint": {
		"query_data": """SELECT s.id, b.id, m.story_point_field
                            FROM jira.sprints s
                            JOIN jira.boards b
                            ON s.board_id = b.id
                            JOIN jira.projects p
                            ON b.project_id = p.id
                            JOIN jira.projects_type_keys ptk
                            ON p.type_key_id = ptk.id
                            JOIN jira.projects_styles ps
                            ON p.style_id = ps.id
                            JOIN jira.project_type_style_mapping m
                            ON ps.style = m.style;""",
		"get_all_data_function": False,
		"get_data_with_details_function": get_needed_details_of_all_issues,
		"columns_to_normalize": ["type", "status_category", "status", "priority", "epic_name"],
		"aux_tables_names": ["issues_types", "issues_status_categories", "issues_statuses", "issues_priorities", "issues_epic_names"],
        "foreign_to_rename": {
            "type": "type_id",
            "status_category": "status_category_id",
            "status": "status_id",
            "priority": "priority_id",
            "epic_name": "epic_name_id"
        },
        "date_columns": ["created", "last_updated"],
        "schema": "jira",
        "table_name": "issues"
	},
	"issues_board": {
		"query_data": None,
		"get_all_data_function": False,
		"get_data_with_details_function": get_needed_details_of_all_issues,
		"columns_to_normalize": ["status_category", "status", "priority", "epic_name"],
		"aux_tables_names": ["issues_status_categories", "issues_statuses", "issues_priorities", "issues_epic_names"],
        "schema": "jira",
        "table_name": "issues"
	}
}