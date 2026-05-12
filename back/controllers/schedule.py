from flask import Blueprint, request, jsonify
from models import schedule as ScheduleModel

schedule_bp = Blueprint('schedule', __name__)

@schedule_bp.get('/api/schedules')
def get_schedules():
    usercode = request.args.get('usercode')
    data     = ScheduleModel.get_schedules(usercode)
    return jsonify(data)

@schedule_bp.post('/api/schedules')
def add_schedule():
    data = request.json
    ScheduleModel.insert_schedule(
        data['usercode'],
        data['title'],
        data['date'],
        data.get('description', '')
    )
    return jsonify({"success": True, "message": "일정이 추가되었습니다."})

@schedule_bp.delete('/api/schedules/<int:scd_no>')
def delete_schedule(scd_no):
    usercode = request.args.get('usercode')
    ScheduleModel.remove_schedule(scd_no, usercode)
    return jsonify({"success": True, "message": "일정이 삭제되었습니다."})
