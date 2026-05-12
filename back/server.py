from flask import Flask, send_from_directory
from controllers.auth import auth_bp
from controllers.schedule import schedule_bp
from controllers.chat import chat_bp

app = Flask(__name__)

# Blueprint 등록
app.register_blueprint(auth_bp)
app.register_blueprint(schedule_bp)
app.register_blueprint(chat_bp)

# 프론트엔드 서빙
@app.route('/')
def index():
    return send_from_directory('../front', 'index.html')

@app.route('/src/<path:filename>')
def src_files(filename):
    return send_from_directory('../src', filename)

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('../front', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
