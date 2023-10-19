"""
It takes the data from the hrplus.glb_emails_for_app view and it performs a safe truncate_insert the employee_app.employee_table.
Then it performs an insert statement to add extra needed data.
"""

import pandas as pd
import utils.dbutils as dbutils
import utils.dfutils as dfutils


def update_employee_app_employee_table(schema, target_table):
    print("Opening database connection.")
    conn = dbutils.open_connection_with_scripting_account()
    query = """SELECT first_name AS name,
       last_name,
       NULL as phone_number,
       address AS email,
       NULL AS status,
       CAST(badge_number AS int) AS employee_id,
       section_name
    FROM hrplus.glb_emails_for_app
    WHERE badge_number LIKE '[0-9]%';"""
    print("Obtaining the data from hrplus.glb_emails_for_app view")
    df = pd.read_sql(query, conn)
    df = dfutils.fill_dataframe_nulls(df)
    print(df)
    
    insert_statement = f"INSERT INTO {schema}.{target_table} (name, last_name, email, employee_id) VALUES (?, ?, ?, ?)"
    values = [
        ('Yasmine','Brown','Yasmine.brown19@yahoo.com','119991551'),
        ('Katerine','Urbano','katerine.urbano@itelinternational.com','2'),
        ('Marlon','Mendez','marlon.mendez@itelinternational.com','111'),
        ('Sancia', 'Powell-Davis', 'Torontoayana@gmail.com', '120442990'),
        ('Test','Test','Test1@mailinator.com','3'),
        ('Test','Test','Test2@mailinator.com','4'),
        ('Test','Test','Test3@mailinator.com','5'),
        ('Test','Test','Test4@mailinator.com','6'),
        ('Test','Test','Test5@mailinator.com','7'),
        ('Test','Test','Test6@mailinator.com','8'),
        ('Test','Test','Test7@mailinator.com','9'),
        ('Test','Test','Test8@mailinator.com','10'),
        ('Test','Test','Test9@mailinator.com','11'),
        ('Test','Test','Test10@mailinator.com','12'),
        ('Test','Test','Test11@mailinator.com','13'),
        ('Test','Test','Test12@mailinator.com','14')
    ]
    try:
        dbutils.perform_safe_truncate_insert(df, conn, schema=schema, target_table_name=target_table)
        print("Opening a new database connection.")
        conn = dbutils.open_connection_with_scripting_account()
        cursor = conn.cursor()
        for value in values:
            print(f"Inserting: {value}")
            cursor.execute(insert_statement, value)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Oops! Something went wrong: {e}")
    
    

def main(optional: list):
    """ Runs the update_employee_app_employee_table.
    Args:
        optional (int): Run mode.
    """

    match optional[0]:
        case 1:
            schema = "employee_app"
            target_table = "employee_table"
            update_employee_app_employee_table(schema, target_table)