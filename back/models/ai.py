import ollama

def get_stream(question):
    return ollama.chat(
        model='gemma2',
        messages=[{'role': 'user', 'content': question}],
        stream=True
    )
