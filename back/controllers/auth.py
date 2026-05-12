from flask import Blueprint, request, jsonify
from models import user as UserModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.post('/api/login')
def login():
    data   = request.json
    result = UserModel.find_user(data['id'])

    if result is None:
        return jsonify({"success": False, "message": "존재하지 않는 아이디입니다."})
    elif result['USER_PW'] == data['pw']:
        return jsonify({"success": True, "usercode": result['USER_CODE'], "grant": result['USER_GRANT']})
    else:
        return jsonify({"success": False, "message": "비밀번호가 틀렸습니다."})

@auth_bp.post('/api/signup')
def signup():
    data    = request.json
    success = UserModel.create_user(data['id'], data['pw'])

    if success:
        return jsonify({"success": True, "message": "계정이 생성되었습니다."})
    else:
        return jsonify({"success": False, "message": "중복되는 아이디가 존재합니다."})
