import ollama

MODEL = 'gemma2:9b'

def chat_json(system_prompt, user_message):
    res = ollama.chat(
        model=MODEL,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user',   'content': user_message}
        ],
        format='json'
    )
    return res['message']['content']
