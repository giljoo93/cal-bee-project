from flask import Blueprint, request, Response
from models import ai as AIModel

chat_bp = Blueprint('chat', __name__)

@chat_bp.post('/api/chat')
def chat():
    question = request.json.get('question')

    def generate():
        stream = AIModel.get_stream(question)
        for chunk in stream:
            yield chunk['message']['content']

    return Response(generate(), mimetype='text/plain')
