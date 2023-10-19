# import packages
import src.health_safety.funtions.live_excels_functions as live_excels_functions
import numpy as np

configs = {
    "bus_arrival_departure_log": {
        "read_with_dtype": {
            "ID": "str",
            "Number of Passengers Being Transported": "int64",
            "Report Date": "datetime64",
            "Departure Time": "str",
            "Arrival Time": "str",
            "Transportation Category": "str",
            "Pick-up Location (s).": "str",
            "Final Destination": "str",
            "Transportation Company": "str",
            "Driver's Name": "str",
            "Vehicle Type": "str",
            "Driver's License Plate Number.": "str",
            "Comment/Recommendation/Concerns": "str"
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "ID",
                    "Report Date",
                    "Transportation Category",
                    "Pick-up Location (s).",
                    "Final Destination",
                    "Transportation Company",
                    "Driver's Name",
                    "Number of Passengers Being Transported",
                    "Departure Time",
                    "Arrival Time",
                    "Vehicle Type",
                    "Driver's License Plate Number.",
                    "Comment/Recommendation/Concerns"
                ],
                "rename_columns": {
                    "ID": "id",
                    "Number of Passengers Being Transported": "number_of_passengers_being_transported",
                    "Report Date": "report_date",
                    "Departure Time": "departure_time",
                    "Arrival Time": "arrival_time",
                    "Transportation Category": "transportation_category",
                    "Pick-up Location (s).": "pick_up_location",
                    "Final Destination": "final_destination",
                    "Transportation Company": "transportation_company",
                    "Driver's Name": "driver_name",
                    "Vehicle Type": "vehicle_type",
                    "Driver's License Plate Number.": "driver_license_plate_number",
                    "Comment/Recommendation/Concerns": "comment_recommendation_concerns"
                },
                "validate_int_columns": [
                    "number_of_passengers_being_transported"
                ],
                "validate_date_columns": {
                    "columns": [
                        "report_date"
                    ],
                    "parameters": {
                        "date_format": "%m/%d/%Y"
                    }
                },
                "validate_text_columns": [
                    "id",
                    "transportation_category",
                    "pick_up_location",
                    "final_destination",
                    "transportation_company",
                    "driver_name",
                    "vehicle_type",
                    "driver_license_plate_number",
                    "comment_recommendation_concerns",
                    "departure_time",
                    "arrival_time"
                ]
            }
                
        },
        "transform_function": live_excels_functions.transforms_function_bus_arrival_departure_log
    },
    "vehicle_capacities":{
        "read_with_dtype": {
            "capacity": "int64",
            "vehicle_name": "str"
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "vehicle_name",
                    "capacity"
                ],
                "validate_int_columns": [
                    "capacity"
                ],
                "validate_text_columns": [
                    "vehicle_name"
                ]
            }
                
        },
        "transform_function": live_excels_functions.transforms_function_vehicle_capacities       
    },
    "trip_costs":{
        "read_with_dtype": {
            "costs": "str",
            "transportation_company": "str",
            "vehicle_type": "str",
            "pickup_location": "str",
            "final_destination": "str",
            "type": "str",
            "currency": "str"
        },
        "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "transportation_company",
                    "vehicle_type",
                    "pickup_location",
                    "final_destination",
                    "costs",
                    "type",
                    "currency"
                ],
                "validate_int_columns": [
                    "costs"
                ],
                "validate_text_columns": [
                    "transportation_company",
                    "vehicle_type",
                    "pickup_location",
                    "final_destination",
                    "type",
                    "currency"
                ]
            }
                
        },
        "transform_function": live_excels_functions.transforms_function_trip_costs         
    },
    "honduras_trip_cost": {
        "read_with_dtype": {
            "hon_id": "str",
            "date_begin": "datetime64",
            "date_end": "datetime64",
            "route_name": "str",
            "pick_up_location": "str",
            "final_destination": "str",
            "transportation_company": "str",
            "driver_name": "str",
            "site_id": "str",
            "vehicle_type": "str",
            "cost": "int64",
            "currency": "str",
            "number_of_passengers_being_transported": "int64"
        },
         "info_transform_function": {
            "df_handling": {
                "order_columns": [
                    "hon_id",
                    "date_begin",
                    "date_end",
                    "route_name",
                    "pick_up_location",
                    "final_destination",
                    "transportation_company",
                    "driver_name",
                    "site_id",
                    "vehicle_type",
                    "cost",
                    "currency",
                    "number_of_passengers_being_transported"    
                ],
                "validate_int_columns": [
                    "cost",
                    "number_of_passengers_being_transported"
                ],
                "validate_text_columns": [
                    "hon_id",
                    "route_name",
                    "pick_up_location",
                    "final_destination",
                    "transportation_company",
                    "driver_name",
                    "site_id",
                    "vehicle_type",
                    "currency"
                ],
                "validate_date_columns": {
                    "columns": [
                        "date_begin",
                        "date_end"
                    ],
                    "parameters": {
                        "date_format": "%m/%d/%Y"
                    }
                },
            }            
        },
    "transform_function": live_excels_functions.transforms_function_honduras_trip_cost
    }
}