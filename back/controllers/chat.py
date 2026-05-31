import json
from datetime import date
from flask import Blueprint, request, jsonify
from models import ai as AIModel
from models import schedule as ScheduleModel

chat_bp = Blueprint('chat', __name__)

SYSTEM_TEMPLATE = """너는 'cal-bee'라는 한국어 일정 관리 비서다.
사용자의 메시지를 보고 의도를 분류해 **JSON 한 개**로만 응답한다. 다른 텍스트는 절대 출력하지 않는다.

오늘 날짜: {today}

사용자의 현재 일정 목록:
{schedules}

응답 스키마:
{{
  "action": "add" | "delete" | "list" | "chat",
  "title": "일정 제목 (action=add 일 때 필수)",
  "date": "YYYY-MM-DD (action=add 일 때 필수)",
  "description": "상세 설명 (선택)",
  "scd_no": 정수 (action=delete 일 때 필수, 위 목록의 SCD_NO 사용),
  "reply": "사용자에게 보여줄 한국어 답변 (항상 필수)"
}}

규칙:
- 새 일정을 추가/등록/잡아달라는 요청이면 action=add. 날짜가 모호하면("내일", "다음주 금요일") 오늘 날짜 기준으로 정확한 YYYY-MM-DD로 변환.
- 특정 일정을 삭제/취소/지워달라는 요청이면 action=delete. 위 목록에서 가장 일치하는 SCD_NO를 골라라.
- 일정을 보여달라/뭐 있냐 같은 조회 요청이면 action=list.
- 위 어느 것도 아니면(잡담, 질문 등) action=chat.
- 정보가 부족해서 add/delete 를 못 하면 action=chat 으로 무엇이 부족한지 reply 에 한국어로 묻는다.
- reply 는 자연스러운 한국어 한두 문장으로."""


def _build_system_prompt(schedules):
    if not schedules:
        sched_text = "(없음)"
    else:
        lines = [
            f"- SCD_NO={s['SCD_NO']}, 제목='{s['SCD_TITLE']}', 날짜={s['SCD_DATE']}, 설명='{s.get('DESCRIPTION', '')}'"
            for s in schedules
        ]
        sched_text = "\n".join(lines)
    return SYSTEM_TEMPLATE.format(today=date.today().isoformat(), schedules=sched_text)


def _safe_parse(raw):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find('{')
        end   = raw.rfind('}')
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw[start:end + 1])
            except json.JSONDecodeError:
                return None
        return None


@chat_bp.post('/api/chat')
def chat():
    body     = request.json or {}
    question = (body.get('question') or '').strip()
    usercode = body.get('usercode')

    if not question:
        return jsonify({"reply": "메시지를 입력해 주세요.", "refresh": False})

    if not usercode:
        return jsonify({"reply": "로그인이 필요합니다.", "refresh": False})

    schedules = ScheduleModel.get_schedules(usercode)
    system    = _build_system_prompt(schedules)

    raw    = AIModel.chat_json(system, question)
    parsed = _safe_parse(raw)

    if not parsed:
        return jsonify({"reply": "죄송해요, 이해하지 못했어요. 다시 말씀해 주세요.", "refresh": False})

    action = parsed.get('action', 'chat')
    reply  = parsed.get('reply') or '처리했어요.'

    if action == 'add':
        title    = parsed.get('title')
        scd_date = parsed.get('date')
        desc     = parsed.get('description', '') or ''
        if not title or not scd_date:
            return jsonify({"reply": "일정 제목과 날짜를 알려 주세요.", "refresh": False})
        ScheduleModel.insert_schedule(usercode, title, scd_date, desc)
        return jsonify({"reply": reply, "refresh": True})

    if action == 'delete':
        scd_no = parsed.get('scd_no')
        if scd_no is None:
            return jsonify({"reply": "어떤 일정을 삭제할지 알려 주세요.", "refresh": False})
        ScheduleModel.remove_schedule(scd_no, usercode)
        return jsonify({"reply": reply, "refresh": True})

    return jsonify({"reply": reply, "refresh": False})
