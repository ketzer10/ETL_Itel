import pandas as pd
import utils.dfutils as dfutils


def transform_studio_ivr_data(df, contacts, agent_options, categories, ss_audios):
    print(f"Transforming Studio Flow Execution report data for IVR")
    # Calls that have an option to speak with an agent in their flow
    agents_ids = df[df["Exit"].isin(agent_options)]["Interaction_ID"].unique().tolist()
    # Calls that don't have any option to speak with an agent in their flow
    no_agent_ids = df[~df["Interaction_ID"].isin(agents_ids)]["Interaction_ID"].unique()
    # DF with calls that don't have any option to speak with an agent in their flow
    df_no_agents = df[df["Interaction_ID"].isin(no_agent_ids)]
    # Calls that accessed the IVR Main Menu and don't have any option to speak with an agent in their flow
    main_menu_ids = df_no_agents[(df_no_agents["Step Name"] == "IVR Main Menu")]["Interaction_ID"].unique().tolist()
    # DF with calls that accesed the IVR Main Menu and don't have any option to speak with an agent in their flow
    df_main_menu = df_no_agents[df_no_agents["Interaction_ID"].isin(main_menu_ids)]
    # Calls that have any category (First level option) in their flow
    main_menu_cats_ids = df_main_menu[df_main_menu["Exit"].isin(categories.keys())]["Interaction_ID"].unique().tolist()
    # Calls that accessed the IVR Main Menu but don't have any category (First level option) in their flow
    main_menu_no_cats_ids = df_main_menu[~df_main_menu["Interaction_ID"].isin(main_menu_cats_ids)]["Interaction_ID"].unique().tolist()
    # Calls where the customer NEVER accessed the IVR Main Menu
    no_main_menu_ids = df_no_agents[~df_no_agents["Interaction_ID"].isin(main_menu_ids)]["Interaction_ID"].unique().tolist()
    # Calls that accessed the IVR Main Menu but don't have any category in their flow + Calls that NEVER accesed the IVR Main Menu
    no_main_menu_and_no_main_menu_cats_ids = set(no_main_menu_ids + main_menu_no_cats_ids)
    # DF that have the profile details calls and other IVR calls
    possible_profile_only_df = df_no_agents[(df_no_agents["Interaction_ID"].isin(no_main_menu_and_no_main_menu_cats_ids))]
    # Calls where the customer received any information related to their account without entering the IVR Main Menu or choosing any first level option from the IVR Main Menu
    profile_only_ids = possible_profile_only_df[possible_profile_only_df["Step Name"].isin(ss_audios)]["Interaction_ID"].unique().tolist()
    # These are Other IVR Calls
    other_ids = possible_profile_only_df[~possible_profile_only_df["Interaction_ID"].isin(profile_only_ids)]["Interaction_ID"].unique().tolist()
    # These are IVR Abandoned Calls
    ivr_abandoned_ids = (set(df[df["Exit"].isin(agent_options)]["Interaction_ID"])
                         - set(contacts[(contacts["contact_type"].isin(["Answered", "Abandoned", "Short Abandoned", "Missed"])) & (contacts["direction"] == "IN")]["interaction_id"]))
    
    def get_type_of_call(row):
        if row['Interaction_ID'] in main_menu_cats_ids:
            return 'Main Menu'
        elif row['Interaction_ID'] in profile_only_ids:
            return 'Profile only'
        elif row['Interaction_ID'] in other_ids:
            return 'Other IVR'
        elif row["Interaction_ID"] in ivr_abandoned_ids:
            return "IVR Abandoned"
        else:
            return pd.NA
    
    df_call_types = df[["Interaction_ID", "started_at_utc"]].drop_duplicates()
    df_call_types['type_of_call'] = df_call_types.apply(get_type_of_call, axis=1)
    df_call_types.columns = list(map(lambda x: x.lower(), df_call_types.columns))
    df_call_types_to_merge = df_call_types[["interaction_id", "type_of_call"]].copy()
    cat_helper_df = create_categories_helper_df(categories)
    touchpoints_df = count_touchpoints(df, cat_helper_df, categories)
    df_to_load = generate_final_df_to_load(touchpoints_df, df_call_types_to_merge, df_call_types)
    df_to_load["type_of_call"] = df_to_load.type_of_call.fillna("Handled by agent")
    print(df_to_load)
    
    return df_to_load
    

# To create a helper dataframe which will be useful to count the touchpoints
def create_categories_helper_df(categories):
    help_data = []
    for category in categories.keys():
        row = [category, "place_holder"]
        help_data.append(row)
        for sub in categories[category]:
            row = [sub, category]
            row_2 = [category, "place_holder"]
            help_data.append(row)

    cat_helper_df = pd.DataFrame(help_data, columns=["Exit", "Category"])
    
    return cat_helper_df

# To transform the contacts report to upload it to the database
def transform_contacts_data(contacts, contacts_columns_to_load, filter_ring_groups):
    contacts = contacts[contacts["Ring Groups"].isin(filter_ring_groups)].copy()
    contacts = contacts[contacts_columns_to_load].copy()
    contacts.columns = list(map(lambda x: x.replace(" ", "_").lower(), contacts.columns))
    
    return contacts

# To count touchpoints (First and Second level IVR Main Menu options) from studio data
def count_touchpoints(df, cat_helper_df, categories):
    test_df = df.merge(cat_helper_df, how="left", on="Exit")
    test_df = test_df.dropna().copy()
    test_df = test_df[["started_at_utc", "Interaction_ID", "Category", "Exit"]].copy()
    test_df.columns = ["started_at_utc", "interaction_id", "category", "subcategory"]
    subs = cat_helper_df[~cat_helper_df.Exit.isin(categories.keys())]["Exit"].unique()
    place_holders_count = test_df[test_df.category == "place_holder"].groupby("interaction_id")["interaction_id"].count()
    sub_count = test_df[test_df.subcategory.isin(subs)].groupby("interaction_id")["interaction_id"].count()
    diff = place_holders_count - sub_count
    no_option_1 = list(set(place_holders_count.index) - set(sub_count.index))
    no_option_2 = list((diff[diff > 0]).index)
    test_df.loc[(test_df.interaction_id.isin(no_option_1)) & (test_df.category == "place_holder"), "category"] = "No option selected"
    condition = test_df["category"] == "No option selected"
    temp = test_df.loc[condition, "subcategory"].copy()
    test_df.loc[condition, 'subcategory'] = test_df.loc[condition, 'category']
    test_df.loc[condition, 'category'] = temp
    extract = test_df[test_df.interaction_id.isin(no_option_2)].copy()
    extract.loc[extract.groupby('interaction_id').tail(1).index, 'category'] = 'No option selected'
    extract = extract[extract.category != "place_holder"]
    condition = extract["category"] == "No option selected"
    temp = extract.loc[condition, "subcategory"].copy()
    extract.loc[condition, 'subcategory'] = extract.loc[condition, 'category']
    extract.loc[condition, 'category'] = temp
    test_df = test_df[test_df.category != "place_holder"].copy()
    test_df = test_df[~test_df.interaction_id.isin(no_option_2)].copy()
    touch_points_df = pd.concat([test_df, extract])
    
    return touch_points_df


def generate_final_df_to_load(touchpoints_df, df_call_types_to_merge, df_call_types):
    touchpoints_calls = touchpoints_df.merge(df_call_types_to_merge, on="interaction_id", how="left")
    no_touchpoints_calls = df_call_types[~df_call_types.interaction_id.isin(touchpoints_calls.interaction_id.unique())].copy()
    no_touchpoints_calls["category"] = "No touchpoint"
    no_touchpoints_calls["subcategory"] = "No touchpoint"
    no_touchpoints_calls = no_touchpoints_calls[["started_at_utc", "interaction_id", "category", "subcategory", "type_of_call"]]
    df_to_load = pd.concat([touchpoints_calls, no_touchpoints_calls])
    
    return df_to_load


def transform_contacts_data(contacts: pd.DataFrame, contacts_columns_to_load: list, rename_columns: dict):
    print(f"Transforming Contacts report data for Calls")
    contacts = contacts[contacts_columns_to_load].copy()
    contacts.columns = list(map(lambda x: x.replace(" ", "_").lower(), contacts.columns))
    # rename_columns = reports_configs["contacts"]["rename_columns"]
    contacts.rename(columns=rename_columns, inplace=True)
    contacts = dfutils.validate_datetime_columns(contacts, columns=["started_at_utc"], date_format="%Y-%m-%d %H:%M:%S")
    contacts = dfutils.fill_dataframe_nulls(contacts)
    
    return contacts

def transform_studio_chat_data(df: pd.DataFrame, flow_column: str, flow_name: str, timestamp_column: str, escalations: list, subs_to_replace: dict):
    chat = df[df[flow_column] == flow_name].copy()
    chat["started_at_utc"] = chat.groupby("Interaction_ID")[timestamp_column].transform("min")
    chat["started_at_utc"] = pd.to_datetime(chat["started_at_utc"])


    ## Interaction with agents

    inter_agents_ids = chat[chat.Exit == "chat_started"].Interaction_ID.unique()
    inter_agents_df = chat[(chat.Interaction_ID.isin(inter_agents_ids))
                        & (chat["Step Name"] == "Reporting Reason")
                        & (chat.Exit.isin(escalations))][["started_at_utc", "Interaction_ID", "Exit"]]
    inter_agents_df.rename(columns={"Exit": "subcategory"}, inplace=True)
    inter_agents_df.insert(loc=2, column="category", value="Interaction with agents")
    inter_agents_df["subcategory"] = inter_agents_df.subcategory.replace(to_replace=subs_to_replace)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    ## No interaction with agents

    # After business hours
    after_hours_ids = chat[(chat["Component Title"] == "Time Based Rules") & (chat.Exit == "no-match")].Interaction_ID.unique()
    after_hours_df = chat[chat.Interaction_ID.isin(after_hours_ids)][["started_at_utc", "Interaction_ID"]].drop_duplicates()
    after_hours_df["category"] = "No interaction with agents"
    after_hours_df["subcategory"] = "After business hours"
    
    # Holidays
    holidays_ids = chat[(chat["Component Title"] == "Calendar Based Rules") & (chat.Exit == "Holiday")].Interaction_ID.unique()
    holidays_df = chat[chat.Interaction_ID.isin(holidays_ids)][["started_at_utc", "Interaction_ID"]].drop_duplicates()
    holidays_df["category"] = "No interaction with agents"
    holidays_df["subcategory"] = "Holiday"

    # Only virtual agent
    only_va_ids = chat[(chat["Step Name"] == "JPS VA") & (chat.Exit == "success")].Interaction_ID.unique()
    only_va_df = chat[chat.Interaction_ID.isin(only_va_ids)][["started_at_utc", "Interaction_ID"]].drop_duplicates()
    only_va_df["category"] = "No interaction with agents"
    only_va_df["subcategory"] = "Only virtual agent"

    # Error in the JPS VA Step Name (Error)
    error_va_exits = ["error", "failure"]
    error_va_ids = chat[(chat["Step Name"] == "JPS VA") & (chat.Exit.isin(error_va_exits))].Interaction_ID.unique()
    error_va_df = chat[chat.Interaction_ID.isin(error_va_ids)][["started_at_utc", "Interaction_ID"]].drop_duplicates()
    error_va_df["category"] = "No interaction with agents"
    error_va_df["subcategory"] = "Error"

    # No agents available
    time_limit_ids = chat[(chat.Exit == "time_limit_reached") & (chat["Step Name"] == "A&D Queue JPS chat")].Interaction_ID.unique()
    no_match_ids = chat[(chat.Exit == "no_match") & (chat["Step Name"] == "A&D Queue JPS chat")].Interaction_ID.unique()
    no_answer_ids = chat[(chat.Exit == "no_answer") & (chat["Step Name"] == "A&D Queue JPS chat")].Interaction_ID.unique()
    no_agents_available_df = chat[(chat.Interaction_ID.isin(time_limit_ids))
                                | (chat.Interaction_ID.isin(no_match_ids))
                                | (chat.Interaction_ID.isin(no_answer_ids))][["started_at_utc", "Interaction_ID"]].drop_duplicates()
    no_agents_available_df["category"] = "No interaction with agents"
    no_agents_available_df["subcategory"] = "No agents available"

    # Error after Time and Calendar validation (Error)
    error_after_val_ids = chat[(chat.Exit == "error") & (chat["Step Name"] == "A&D Queue JPS chat")].Interaction_ID.unique()
    error_after_val_df = chat[chat.Interaction_ID.isin(error_after_val_ids)][["started_at_utc", "Interaction_ID"]].drop_duplicates()
    error_after_val_df["category"] = "No interaction with agents"
    error_after_val_df["subcategory"] = "Error"

    data_to_upload = pd.concat([inter_agents_df, after_hours_df, only_va_df, error_va_df, no_agents_available_df, error_after_val_df, holidays_df])
    data_to_upload.rename(columns={"Interaction_ID": "interaction_id"}, inplace=True)

    return data_to_upload