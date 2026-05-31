from models.db import with_db
from datetime import date

def _to_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return v

@with_db
def get_schedules(data, usercode):
    uc = _to_int(usercode)
    return [dict(s) for s in data['schedule'] if s['USER_CODE'] == uc]

@with_db
def insert_schedule(data, usercode, title, scd_date, description):
    scd_no = data['meta']['next_scd_no']
    data['meta']['next_scd_no'] = scd_no + 1
    today = str(date.today())
    data['schedule'].append({
        "USER_CODE":   _to_int(usercode),
        "SCD_NO":      scd_no,
        "SCD_TITLE":   title,
        "SCD_DATE":    str(scd_date),
        "SCD_TIME":    None,
        "DESCRIPTION": description,
        "CREATED_AT":  today,
        "UPDATED_AT":  today
    })

@with_db
def remove_schedule(data, scd_no, usercode):
    uc = _to_int(usercode)
    sn = _to_int(scd_no)
    data['schedule'] = [
        s for s in data['schedule']
        if not (s['SCD_NO'] == sn and s['USER_CODE'] == uc)
    ]
