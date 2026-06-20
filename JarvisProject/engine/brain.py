import ollama
from engine.memory import retrieve_memory, store_info

def chat_with_ai(user_input, visual_context=""):
    past_memory = retrieve_memory(user_input)
    
    if "remember that" in user_input.lower():
        return store_info(user_input.replace("remember that", ""))

    system_prompt = f"You are JARVIS. Context from memory: {past_memory}. Visual Context: {visual_context}"
    
    response = ollama.chat(model='llama3.2', messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_input},
    ])
    return response['message']['content']