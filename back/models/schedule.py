from models.db import get_connection
from datetime import date

def get_schedules(usercode):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM schedule WHERE USER_CODE = %s", (usercode,))
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        row['SCD_DATE']   = str(row['SCD_DATE'])
        row['CREATED_AT'] = str(row['CREATED_AT'])
        row['UPDATED_AT'] = str(row['UPDATED_AT'])
    return rows

def insert_schedule(usercode, title, scd_date, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO schedule "
        "(USER_CODE, SCD_NO, SCD_TITLE, SCD_DATE, SCD_TIME, DESCRIPTION, CREATED_AT, UPDATED_AT) "
        "VALUES (%s, null, %s, %s, null, %s, %s, %s)",
        (usercode, title, scd_date, description, date.today(), date.today())
    )
    conn.commit()
    conn.close()

def remove_schedule(scd_no, usercode):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM schedule WHERE SCD_NO = %s AND USER_CODE = %s",
        (scd_no, usercode)
    )
    conn.commit()
    conn.close()
