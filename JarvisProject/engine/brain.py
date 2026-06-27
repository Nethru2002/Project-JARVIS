import ollama
from config.settings import JARVIS_PROMPT
from engine.memory import get_memory_string

chat_history = []

def chat_with_ai(user_input, visual_context=""):
    global chat_history
    
    long_term_mem = get_memory_string()
    
    system_msg = f"{JARVIS_PROMPT}\n{long_term_mem}\nRecent Chat: {chr(10).join(chat_history[-5:])}"
    
    if visual_context:
        system_msg += f"\n[JARVIS IS LOOKING AT]: {visual_context}"

    try:
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': system_msg},
            {'role': 'user', 'content': user_input},
        ])
        
        reply = response['message']['content']
        
        chat_history.append(f"User: {user_input}")
        chat_history.append(f"Jarvis: {reply}")
        
        return reply
    except Exception as e:
        return f"I'm having a bit of a brain fog, sir. Error: {e}"