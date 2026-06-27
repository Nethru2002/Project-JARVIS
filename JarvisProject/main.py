import threading
import sys
import datetime
import time

from engine.speech import speak, listen, choose_best_microphone
from engine.brain import chat_with_ai
from engine.actions import execute_command
from engine.vision import capture_and_analyze
from engine.wake_word import wait_for_wake_word
from engine.security import verify_user
from engine.web_agent import research_topic
from gui.interface import JarvisUI
from config.settings import PASSCODE, USER_NAME, get_random_status

is_initialized = False
chat_history = []

def get_time_greeting():
    hour = datetime.datetime.now().hour
    if hour < 12: return "Good morning"
    if hour < 18: return "Good afternoon"
    return "Good evening"

def jarvis_logic(ui):
    global is_initialized
    is_initialized = True
    
    ui.start_btn.configure(state="disabled", text="NEXUS ACTIVE")
    ui.terminal_log("SCANNING HARDWARE TOPOLOGY...")
    
    best_mic = choose_best_microphone()
    ui.terminal_log(f"PRIMARY INPUT SECURED ON DEVICE {best_mic}")
    
    ui.update_status("[ SCANNING ]", "#ffcc00")
    auth_result = verify_user()
    is_authorized = False

    if auth_result == "Authorized":
        is_authorized = True
    else:
        ui.update_status("[ CHALLENGE ]", "#ffcc00")
        speak(f"Biometric mismatch. {USER_NAME}, initiate manual override.")
        
        vocal_input = listen()
        manual_input = ui.pass_entry.get()

        if PASSCODE in vocal_input.lower() or manual_input == PASSCODE:
            is_authorized = True
            ui.pass_entry.delete(0, 'end')
        else:
            ui.update_status("[ LOCKED ]", "#ff3333")
            speak("Security violation. Critical shutdown.")
            time.sleep(2)
            sys.exit()

    if is_authorized:
        ui.update_status("[ ACTIVE ]", "#00fbff")
        ui.terminal_log(f"IDENTITY VERIFIED: {USER_NAME}")
        
        greeting = f"{get_time_greeting()}, {USER_NAME}. {get_random_status()}"
        speak(greeting)

    while True:
        ui.update_status("[ MONITORING ]", "#007a7a")
        
        if wait_for_wake_word():
            ui.update_status("[ LISTENING ]", "#ff00ff")
            speak("Online.")
            
            query = listen()
            if not query or len(query) < 2:
                continue

            ui.terminal_log(f"USER: {query}")
            ui.update_status("[ THINKING ]", "#ffff00")

            global chat_history
            chat_history.append(f"User: {query}")
            context = "\n".join(chat_history[-10:])

            if any(k in query for k in ["research", "search", "who is"]):
                response = research_topic(query)
            elif any(k in query for k in ["look", "see", "identify"]):
                response = chat_with_ai(query, capture_and_analyze())
            else:
                response = chat_with_ai(context)

            ui.terminal_log(f"AI: {response[:65]}...")
            
            action_feedback = execute_command(response)
            
            if action_feedback:
                speak(action_feedback)
            else:
                speak(response)

            chat_history.append(f"Jarvis: {response}")
            ui.update_status("[ ACTIVE ]", "#00fbff")

def start_threads():
    if not is_initialized:
        threading.Thread(target=jarvis_logic, args=(app,), daemon=True).start()

if __name__ == "__main__":
    app = JarvisUI(start_threads)
    app.bind("<Escape>", lambda e: sys.exit())
    try:
        app.mainloop()
    except KeyboardInterrupt:
        sys.exit()