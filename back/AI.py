import ollama

# 1. 일반 호출 (한 번에 답변 받기)
def ask_calbee(user_question):
    prompt = f"질문: {user_question}"
    
    response = ollama.chat(model='gemma2', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    
    # 딕셔너리에서 실제 텍스트 내용만 쏙 뽑아서 리턴합니다.
    return response['message']['content'] 


# 2. 스트리밍 호출 (타자 치듯 답변 받기 - 추천!)
def get_calbee_stream(user_question):
    # 모델명을 gemma2로 수정하고, 화면 출력(print) 기능은 뺐습니다.
    stream = ollama.chat(
        model='gemma2', 
        messages=[{'role': 'user', 'content': user_question}],
        stream=True
    )
    
    # 만들어진 스트림(데이터 통로) 자체를 반환합니다.
    return stream