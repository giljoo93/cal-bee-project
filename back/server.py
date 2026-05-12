from flask import Flask, request, jsonify, Response, send_from_directory
from datetime import date
import mysql.connector
import ollama

app = Flask(__name__)

# ── DB 연결 ──────────────────────────────────────────
def serverConn():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="1234",
        database="calbee",
        port=3306
    )

# ── 프론트엔드 서빙 ───────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('../front', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('../front', filename)

@app.route('/src/<path:filename>')
def src_files(filename):
    return send_from_directory('../src', filename)
# ── 로그인 ────────────────────────────────────────────
@app.post('/api/login')
def login():
    data = request.json
    conn = serverConn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE USER_ID = %s", (data['id'],))
    result = cursor.fetchone()
    conn.close()

    if result is None:
        return jsonify({"success": False, "message": "존재하지 않는 아이디입니다."})
    elif result['USER_PW'] == data['pw']:
        return jsonify({"success": True, "usercode": result['USER_CODE'], "grant": result['USER_GRANT']})
    else:
        return jsonify({"success": False, "message": "비밀번호가 틀렸습니다."})

# ── 회원가입 ──────────────────────────────────────────
@app.post('/api/signup')
def signup():
    data = request.json
    conn = serverConn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT USER_ID FROM users WHERE USER_ID = %s", (data['id'],))

    if cursor.fetchone():
        conn.close()
        return jsonify({"success": False, "message": "중복되는 아이디가 존재합니다."})

    cursor.execute("INSERT INTO users VALUES (NULL, %s, %s, %s, 2)", (data['id'], data['pw'], date.today()))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "계정이 생성되었습니다."})

# ── 일정 조회 ─────────────────────────────────────────
@app.get('/api/schedules')
def get_schedules():
    usercode = request.args.get('usercode')
    conn = serverConn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM schedule WHERE USER_CODE = %s", (usercode,))
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        row['SCD_DATE'] = str(row['SCD_DATE'])
        row['CREATED_AT'] = str(row['CREATED_AT'])
        row['UPDATED_AT'] = str(row['UPDATED_AT'])
    return jsonify(rows)

# ── 일정 등록 ─────────────────────────────────────────
@app.post('/api/schedules')
def add_schedule():
    data = request.json
    conn = serverConn()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO schedule (USER_CODE, SCD_NO, SCD_TITLE, SCD_DATE, SCD_TIME, DESCRIPTION, CREATED_AT, UPDATED_AT) "
        "VALUES (%s, null, %s, %s, null, %s, %s, %s)",
        (data['usercode'], data['title'], data['date'], data.get('description', ''), date.today(), date.today())
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "일정이 추가되었습니다."})

# ── 일정 삭제 ─────────────────────────────────────────
@app.delete('/api/schedules/<int:scd_no>')
def delete_schedule(scd_no):
    usercode = request.args.get('usercode')
    conn = serverConn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM schedule WHERE SCD_NO = %s AND USER_CODE = %s", (scd_no, usercode))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "일정이 삭제되었습니다."})

# ── AI 채팅 (스트리밍) ────────────────────────────────
@app.post('/api/chat')
def chat():
    question = request.json.get('question')
    def generate():
        stream = ollama.chat(
            model='gemma2',
            messages=[{'role': 'user', 'content': question}],
            stream=True
        )
        for chunk in stream:
            yield chunk['message']['content']
    return Response(generate(), mimetype='text/plain')

# ── 서버 실행 ─────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)