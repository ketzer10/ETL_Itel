from distutils.ccompiler import show_compilers
from multiprocessing.sharedctypes import Value
import re
import requests
import datetime as dt
import pandas as pd
import src.anyone_home.central.config as configs
import json
import utils.dfutils as dfutils
import numpy as np
from bs4 import BeautifulSoup

def get_label_data_parent_based(soup, lookup_text, shop_id) -> str:
    """
    Gets the text associated with a label. If the text is not found it raises a ValueError.

    :param soup: A beautiful soup object. The response of the request.
    :param lookup_text: The text to find in the beautiful soup object. This is usually a data label.
    :param shop_id: The ID of the shop form currently being scraped. This is used only for logging purposes.
    :return: The value associated with the label.
    """
    try:
        # Strip empty spaces because some text comes with leading or trailing spaces
        value = str.strip(soup.find(text=re.compile(lookup_text)).parent.parent.findAll(text=True)[1])
    except Exception as e:
        print(e)
        raise ValueError(f"The following text was not found: {lookup_text} in card with shop id {shop_id}.")

    return value

def get_shop_category(soup, shop_id) -> str:
    """
    Gets the shop category from a modal.

    :param soup: A beautiful soup object. The response of the request.
    :param lookup_text: The text to find in the beautiful soup object. This is usually a data label.
    :param shop_id: The ID of the shop form currently being scraped. This is used only for logging purposes.
    :return: The value associated with the label.
    """
    try:
        # Strip empty spaces because some text comes with leading or trailing spaces

        value = str.strip(soup.findAll("h4", {"class": "modal-title"})[0].text.strip())
    except Exception as e:
        print(e)
        raise ValueError(f"The shop category was not found for card with shop id {shop_id}.")

    return value

def get_card_progress(soup, shop_id) -> str:
    """
    Gets the shop category from a modal.

    :param soup: A beautiful soup object. The response of the request.
    :param lookup_text: The text to find in the beautiful soup object. This is usually a data label.
    :param shop_id: The ID of the shop form currently being scraped. This is used only for logging purposes.
    :return: The value associated with the label.
    """
    try:
        # Strip empty spaces because some text comes with leading or trailing spaces

        element = soup.find(attrs={"role": "progressbar"})
        value =  element["aria-valuenow"]
    except Exception as e:
        print(e)
        raise ValueError(f"Could not find the progress bar for shop id {shop_id}.")

    return value

def get_link_data_parent_based(soup, lookup_text, shop_id) -> str:
    """
    Gets the text associated with a label. The text is contained inside a link. If the text is not found it raises a
    ValueError.

    :param soup: A beautiful soup object. The response of the request.
    :param lookup_text: The text to find in the beautiful soup object. This is usually a data label.
    :param shop_id: The ID of the shop form currently being scraped. This is used only for logging purposes.
    :return: The value associated with the label.
    """
    try:
        # Strip empty spaces because some text comes with leading or trailing spaces
        value = str.strip(soup.find(text=lookup_text).parent.findNext("a").contents[0])
    except Exception as e:
        print(e)
        raise ValueError(f"The following text was not found: {lookup_text} in card with shop id {shop_id}.")

    return value


def get_call_duration_label_based(soup, lookup_text, shop_id) -> float:
    """
    Gets the call duration associated with a label. If the text is not found it raises a ValueError. If the call
    duration is empty it sets a default of 0.0.

    :param soup: A beautiful soup object. The response of the request.
    :param lookup_text: The text to find in the beautiful soup object. This is usually a data label.
    :param shop_id: The ID of the shop form currently being scraped. This is used only for logging purposes.
    :return: A float representing the call duration
    """
    try:
        # Strip empty spaces because some text comes with leading or trailing spaces
        value = str.strip(soup.find(text=lookup_text).parent.parent.findAll(text=True)[1]).replace("sec", "")
    except Exception as e:
        print(e)
        raise ValueError(f"The following text was not found: {lookup_text} in card with shop id {shop_id}.")

    # If the found text is empty the call has no duration so a default of zero is used
    if value is None:
        return 0.0

    if len(value) == 0:
        return 0.0

    # Convert to float. This will fail if the "sec" couldn"t be stripped from the found text.
    try:
        value = float(value)
    except Exception as e:
        print(e)
        raise ValueError(f"Could not convert call duration to type float in card with shop id {shop_id}.")

    return value


def get_input_value_id_based(soup, tag_id, shop_id) -> str:
    """
    Gets the value of an input based on its ID.

    :param soup: A beautiful soup object. The response of the request.
    :param tag_id: The text to find in the beautiful soup object. This is usually a data label.
    :param shop_id: The ID of the shop form currently being scraped. This is used only for logging purposes.
    :return: The value associated with the label.
    """
    try:
        # Strip empty spaces because some text comes with leading or trailing spaces
        value = str.strip(soup.find(id=tag_id).get("value"))
    except Exception as e:
        print(e)
        raise ValueError(f"The following ID was not found: {tag_id} in card with shop id {shop_id}.")

    return value


def get_textbox_value_null_safe(soup, tag_id, shop_id) -> str:
    """
    Gets the value of a textbox given an ID. If the textbox is empty, it returns an empty string. This makes the

    :param soup: A beautiful soup object. The response of the request.
    :param tag_id: The text to find in the beautiful soup object. This is usually a data label.
    :param shop_id: The ID of the shop form currently being scraped. This is used only for logging purposes.
    :return: The value associated with the label.
    """
    # If the tag isn"t found
    try:
        tag = soup.find(id="grader_notes")
    except Exception as e:
        print(e)
        raise ValueError(f"The following ID was not found: {tag_id} in card with shop id {shop_id}.")

    # If the tag is empty
    try:
        text_value = str.strip(tag.findAll(text=True)[0])
    except Exception as e:
        text_value = ""

    return text_value


def get_check_status(the_soupy_soup, checkbox_id, shop_id) -> str:
    """
    Gets the checked status of a checkbox given a beautiful soup object and a checkbox id. This relies on the fact that
    the ID will only be found once.

    :param the_soupy_soup: A beautiful soup object. Usually the content of the request.
    :param checkbox_id: The ID of the checkbox.
    :param shop_id: The ID of the shop form currently being scraped. This is used only for logging purposes.
    :return: String. "Yes" for checked and "No" for unchecked. Doing a boolean would be nice but it would affect the
    existing database structure.
    """
    try:
        check_state = the_soupy_soup.find(id=checkbox_id).has_attr("checked")
    except Exception as e:
        print(e)
        raise ValueError(f"The following checkbox ID was not found: {checkbox_id} in card with shop id {shop_id}.")

    check_value = "Yes" if check_state else "No"
    return check_value


def get_checkbox_row_value(the_soupy_soup, text, shop_id) -> str:
    """
    Gets the value of the checked radio button from a radio group.

    :param the_soupy_soup: A beautiful soup object. Usually the content of the request.
    :param text: The text of the label inside the div which contains the radio group.
    :param shop_id: The ID of the shop form currently being scraped. This is used only for logging purposes.
    :return: String. The stripped value of the checked radio button.
    """
    try:
        radio_row = the_soupy_soup.find(text=re.compile(text)).parent.findNext("div").find_all("input")
        checked_value = ""
        for radio in radio_row:
            if radio.has_attr("checked"):
                checked_value = radio.get("value")
    except Exception as e:
        print(e)
        raise ValueError(f"The following text for radio buttons was not found: {text} in card with shop id {shop_id}.")

    return str.strip(checked_value)


def get_session_cookies(email_address, password) -> str:
    """
    Opens a session to the central website and logins into the website. Returns the authenticated user cookie.

    :param email_address: The email address to use in the log in form.
    :param password: The password to use in the log in form.
    :return: The cookie after successful user authentication.
    """
    login_request = configs.requests["login_request"]
    session = requests.Session()
    login_request["data"]["email_address"] = email_address
    login_request["data"]["password"] = password
    response = session.post(login_request["url"], headers=login_request["headers"],
                            cookies=login_request["cookies"], data=login_request["data"])
    if response.status_code != 200:
        raise ValueError("Couldn't login to the website please verify your credentials. Status code {code}"
                         .format(code=response.status_code))

    cookie = session.cookies.get_dict()["central"]
    return cookie


def safe_request(request_params: dict, origin: str) -> requests.Response:
    """
    Performs a "safe" request. Raises a ValueError if the response status is not 200 or the response content
    is "session expired"

    :param request_params: Dictionary containing the parameters of the request.
    :param origin: Error message passed when function is called to help with logging.
    :return: A request.Response object if the request was successful.
    """
    response = requests.post(request_params["url"], headers=request_params["headers"],
                             cookies=request_params["cookies"], data=request_params["data"])
    if response.status_code != 200:
        raise ValueError(f"There was a problem processing the request to {origin} Status code {response.status_code} "
                         f"{response.reason} ")
    if response.content == b"session expired":
        raise ValueError("There was a problem processing the request to {origin} Status code {code}. The session has "
                         "expired."
                         .format(code=response.status_code, origin=origin))
    return response


def safe_date_conversion(shop_id, account, property, agentname, score, date_text):
    """
    Converts a text to datetime. Handles possible errors
    """
    date = date_text
    try:
        date = dt.datetime.strptime(date_text, "%m/%d/%Y %I:%M %p")
    except Exception as e:
        print(e)
        raise Exception(f"A problem was encountered converting the date for card with shop ID: {shop_id}. "
                        f"Account: {account}. Property: {property}. Agent: {agentname}. Score: {score}.")

    return date

def get_main_table_data(login_cookie, shop_completed_start_date, shop_completed_end_date, shop_type) -> pd.DataFrame:
    """
    Gets the general data of the audits in a date range.

    :param login_cookie: A string containing the cookie of the session.
    :param shop_completed_start_date: The start date to download in "mm/dd/yyyy" format. Inclusive.
    :param shop_completed_end_date: The end date to download in "mm/dd/yyyy" format. Inclusive.
    :param shop_type: Can be either "Maintenance" or "Audit,Leasing" 
    :return: A dataframe containing the general data for the audits in a given date range.
    """

    # Adjust the parameters of the request, initially the limit is set to 1 to avoid overwhelming the server
    rqst_params = configs.requests["main_table_request"]
    rqst_params["cookies"]["central"] = login_cookie
    rqst_params["data"][6] = ("create_shop_category[]", configs.general_params[shop_type]["real_shop_type"])
    rqst_params["data"][19] = ("qa_completed_from_date", shop_completed_start_date)
    rqst_params["data"][20] = ("qa_completed_to_date", shop_completed_end_date)
    rqst_params["data"][35] = ("limit", "1")

    # Perform the first request. This is used to get the total number of rows in the table.
    initial_response = safe_request(rqst_params, "the main table.")

    initial_response = json.loads(initial_response.content)
    audit_count = initial_response["total_count"]
    current_index = 0
    # Perform the request in 1000 increments. It works and it is a reasonable number.
    limit = min(audit_count, 1000)
    df_result = None

    while current_index < audit_count:
        rqst_params["data"][34] = ("startIndex", current_index)
        rqst_params["data"][35] = ("limit", limit)
        temp_response = safe_request(rqst_params, "the main table.")
        temp_response = json.loads(temp_response.content)
        temp_audit_data = temp_response["listData"]
        # Create the pandas dataframe
        if current_index == 0:
            df_result = pd.DataFrame(temp_audit_data)
        else:
            temp_df = pd.DataFrame(temp_audit_data)
            df_result = pd.concat([df_result, temp_df])

        current_index += limit
        limit = min(1000, audit_count - current_index)

    # Get the configs
    params = configs.general_params["main_table"]
    df_result = pd.DataFrame(columns=params["expected_cols"]) if df_result is None else df_result

    # Transform dataframe
    df_result = dfutils.change_dataframe_columns_name(df_result, params["rename_cols"])
    df_result = dfutils.validate_datetime_columns(df_result, params["datetime_cols"], "%m/%d/%Y %I:%M %p")
    df_result = dfutils.validate_float_columns(df_result, params["float_cols"])
    df_result.drop(columns=params["drop_cols"], inplace=True)
    df_result.replace(np.nan, "", inplace=True)

    return df_result

def get_card_info(login_cookie: str, table_record, total_count: int, shop_type: str) -> list:
    """Helper function to scrape the information of a specific HTML card.

    Args:
        login_cookie (str): A string containing the cookie of the session.
        table_record ([type]):  A record from the main table Dataframe. Used to pass the correct parameters to the request.
        total_count (int): A count of total records used to print progress.
        shop_type (str): Shop type either 'Maintenance' or 'Audit,Leasing'

    Returns:
        list: A list with all the card details for the specific shop type
    """

    account = table_record.account
    property = table_record.property
    agent_name = table_record.agent_name
    score = table_record.shop_score
    shop_sfid = table_record.shop_sfid
    case_status = table_record.case_status
    shop_category = table_record.shop_category
    origin = table_record.origin
    position = table_record.index
    sr_pop = table_record.service_request_pop

    # Modify the request params
    rqst_params = configs.requests["detail_card_request"]
    rqst_params['cookies']['central'] = login_cookie
    rqst_params['data']['shopSfid'] = shop_sfid
    rqst_params['data']['caseStatus'] = str.strip(case_status).replace(' ', '+')
    rqst_params['data']['srpop'] = sr_pop
    rqst_params['data']['shopCategory'] = shop_category
    rqst_params['data']['origin'] = origin
    response = safe_request(rqst_params, f"the card details. Shop ID: {shop_sfid}.")
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    # If the shop score is empty just exit because it is probably a closed case.
    if np.isnan(score):
        print(f'Skipping form with shop sfid {shop_sfid} because the score was empty')
        return

    # Get the data from the HTML card that applies to both leasing/audit and maintenance
    qa_form_name = get_label_data_parent_based(soup, 'QA Form Name:', shop_sfid)
    qa_reviewer = get_label_data_parent_based(soup, 'QA Reviewer:', shop_sfid)
    call_skill = get_label_data_parent_based(soup, 'Call Skill:', shop_sfid)
    call_duration = get_call_duration_label_based(soup, 'Call Duration:', shop_sfid)
    supervisor_name = get_input_value_id_based(soup, 'supervisors_name', shop_sfid)
    team_lead_1 = get_input_value_id_based(soup, 'team_lead1', shop_sfid)
    team_lead_2 = get_input_value_id_based(soup, 'team_lead2', shop_sfid)
    grader_notes = get_textbox_value_null_safe(soup, 'grader_notes', shop_sfid)
    prospect_info_completed = get_check_status(soup, 'prospect_info_completed', shop_sfid)
    first_name = get_check_status(soup, 'firstname', shop_sfid)
    last_name = get_check_status(soup, 'lastname', shop_sfid)
    phone_number = get_check_status(soup, 'phone_number', shop_sfid)
    email = get_check_status(soup, 'email', shop_sfid)
    professional = get_checkbox_row_value(soup, 'Professional', shop_sfid)
    call_ending = get_checkbox_row_value(soup, 'Call Ending', shop_sfid)
    care = get_check_status(soup, 'concerned_about_caller', shop_sfid)
    outstanding_shop = get_check_status(soup, 'outstanding_shop', shop_sfid)


    common_fields = [shop_sfid, qa_form_name, qa_reviewer, call_skill, call_duration, supervisor_name, team_lead_1,
    team_lead_2, grader_notes, prospect_info_completed, first_name, last_name, phone_number, email, 
    professional, call_ending, care, outstanding_shop]
    maintenance_fields = []
    audit_leasing_fields = []

    # Maintenance specific fields
    if shop_type == 'maintenance':
        case_creation_datetime = safe_date_conversion(shop_sfid, account, property, agent_name, score,
                                                    get_label_data_parent_based(soup, 'Service Request Creation Date/Time:',
                                                                                shop_sfid))
        property_unit_needing_service = get_check_status(soup, 'property_unit_needing_service', shop_sfid)
        room_area_impacted = get_check_status(soup, 'room_area_impacted', shop_sfid)
        sr_type = get_check_status(soup, 'sr_type', shop_sfid)
        permission_to_enter = get_check_status(soup, 'permission_to_enter', shop_sfid)
        entry_info = get_check_status(soup, 'entry_info', shop_sfid)
        troubleshooting = get_checkbox_row_value(soup, 'Troubleshooting', shop_sfid)
        empathy = get_checkbox_row_value(soup, 'Empathy', shop_sfid)
        navigation_accuracy = get_checkbox_row_value(soup, 'Navigation/Accuracy', shop_sfid)
        work_order_notes = get_checkbox_row_value(soup, 'Work Order Notes', shop_sfid)

        maintenance_fields = [case_creation_datetime, property_unit_needing_service, room_area_impacted, 
        sr_type, permission_to_enter, entry_info, troubleshooting,
        empathy, navigation_accuracy, work_order_notes]

    # Audit leasing specific fields
    elif shop_type == 'audit_leasing':
        case_creation_datetime = safe_date_conversion(shop_sfid, account, property, agent_name, score,
                                                      get_label_data_parent_based(soup, 'Case Creation Date/Time:',
                                                                                  shop_sfid))
        bedandbath = get_check_status(soup, 'bedandbath', shop_sfid)
        pets = get_check_status(soup, 'pets', shop_sfid)
        reason_for_moving = get_check_status(soup, 'reason_for_moving', shop_sfid)
        floorplan_of_interest = get_check_status(soup, 'floorplan_of_interest', shop_sfid)
        rent_range = get_check_status(soup, 'rent_range', shop_sfid)
        move_in = get_check_status(soup, 'move_in', shop_sfid)
        building_value = get_checkbox_row_value(soup, 'Building Value', shop_sfid)
        no_of_occupants = get_check_status(soup, 'no_of_occupants', shop_sfid)
        attempt_showing = get_checkbox_row_value(soup, 'Attempt to Set a Showing', shop_sfid)
        qualification_policies = get_checkbox_row_value(soup, 'Qualifications & Policies', shop_sfid)
        engaging_rapport = get_checkbox_row_value(soup, 'Engaging and Rapport', shop_sfid)
        notes = get_checkbox_row_value(soup, 'Notes', shop_sfid)
        navigation = get_checkbox_row_value(soup, 'Navigation', shop_sfid)
        accuracy = get_checkbox_row_value(soup, 'Accuracy', shop_sfid)

        audit_leasing_fields = [case_creation_datetime, bedandbath, pets, reason_for_moving, floorplan_of_interest,
        rent_range, move_in, building_value, no_of_occupants, attempt_showing, qualification_policies,
        engaging_rapport, notes, navigation, accuracy]
    else:
        raise ValueError('Invalid shop type provided')

    card_details = common_fields + audit_leasing_fields + maintenance_fields
    
    progress = int(float(position) / float(total_count) * 100.0)
    if progress % 5 == 0:
        print(f'Progress {progress}%')

    return card_details

def get_all_card_info(login_cookie: str, main_table_dataframe: pd.DataFrame, shop_type: str) -> pd.DataFrame:
    """
    Gets the information from a collection of cards. Asynchronous function that can process up to 10 cards in parallel

    :param login_cookie: A string containing the cookie of the session.
    :param main_table_dataframe: A dataframe containing all the cards to be downloaded. Used for the shop ID.
    :return: A dataframe containing all the information for all the scraped cards.
    """
    records = main_table_dataframe.to_records()
    cards = []

    for record in records:
        try:
            card_info = get_card_info(login_cookie, record, main_table_dataframe.shape[0], shop_type)
            if card_info is not None:
                cards.append(card_info)
        except Exception as e:
            print(f'Skipping card with shop id {record.shop_sfid}')
            print(e)

    # Convert the list into a pandas dataframe
    common_cols = configs.general_params["common"]["card_cols"]
    shop_specific_cols = configs.general_params[shop_type]["card_cols"]
    columns = common_cols + shop_specific_cols
    df_cards = pd.DataFrame(columns=columns, data=cards)

    # Convert to float
    float_cols = configs.general_params["common"]["float_cols"]
    df_cards = dfutils.validate_float_columns(df_cards, float_cols)

    # Convert to datetime
    float_cols = configs.general_params[shop_type]["datetime_cols"]
    
    return df_cards


def transform_dataframe(df: pd.DataFrame, new_names: dict, timestamp_columns: list) -> pd.DataFrame:
    """
    Drop unnecesary columns, rename columns, and convert timestamp cols to the timestamp.
    :param df: df_consolidated with main table and card data.
    :param new_names: dictionary with old_name:new_name format for maching headers with database table.
    :param timestamp_columns: list of columns to change to datetime format to match database datatypes.
    """

    df.rename(columns=new_names, inplace=True)
    for column in timestamp_columns:
        df[column] = df[column].astype("datetime64[ns]")
    return df