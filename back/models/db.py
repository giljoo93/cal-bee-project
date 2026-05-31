import json
import os
from threading import Lock

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DB_PATH  = os.path.join(DATA_DIR, 'calbee.json')

_lock = Lock()

_DEFAULT = {
    "meta": {"next_user_code": 1, "next_scd_no": 1},
    "users": [],
    "schedule": []
}

def _ensure_file():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DB_PATH):
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(_DEFAULT, f, ensure_ascii=False, indent=2)

def load_db():
    _ensure_file()
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    _ensure_file()
    tmp = DB_PATH + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DB_PATH)

def with_db(fn):
    def wrapper(*args, **kwargs):
        with _lock:
            data = load_db()
            result = fn(data, *args, **kwargs)
            save_db(data)
            return result
    return wrapper
