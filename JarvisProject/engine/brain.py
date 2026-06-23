import ollama
from config.settings import JARVIS_PROMPT

def chat_with_ai(user_input, visual_context=""):
    system_message = JARVIS_PROMPT
    if visual_context:
        system_message += f"\n[VISUAL DATA RECEIVED]: {visual_context}"

    try:
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': system_message},
            {'role': 'user', 'content': user_input},
        ])
        raw_text = response['message']['content']
        return raw_text
    except Exception as e:
        return f"Neural link error: {e}"