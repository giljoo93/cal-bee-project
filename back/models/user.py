from models.db import get_connection
from datetime import date

def find_user(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE USER_ID = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result

def create_user(user_id, user_pw):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT USER_ID FROM users WHERE USER_ID = %s", (user_id,))
    if cursor.fetchone():
        conn.close()
        return False
    cursor.execute(
        "INSERT INTO users VALUES (NULL, %s, %s, %s, 2)",
        (user_id, user_pw, date.today())
    )
    conn.commit()
    conn.close()
    return True
