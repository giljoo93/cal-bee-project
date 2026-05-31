from models.db import with_db
from datetime import date

@with_db
def find_user(data, user_id):
    for u in data['users']:
        if u['USER_ID'] == user_id:
            return u
    return None

@with_db
def create_user(data, user_id, user_pw):
    if any(u['USER_ID'] == user_id for u in data['users']):
        return False
    code = data['meta']['next_user_code']
    data['meta']['next_user_code'] = code + 1
    data['users'].append({
        "USER_CODE":  code,
        "USER_ID":    user_id,
        "USER_PW":    user_pw,
        "CREATED_AT": str(date.today()),
        "USER_GRANT": 2
    })
    return True
