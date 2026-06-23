import threading
import sys
import datetime
import time

from engine.speech import speak, listen
from engine.brain import chat_with_ai
from engine.actions import execute_command
from engine.vision import capture_and_analyze
from engine.wake_word import wait_for_wake_word
from engine.security import verify_user
from engine.web_agent import research_topic
from gui.interface import JarvisUI
from config.settings import PASSCODE, USER_NAME, get_random_status

is_initialized = False

def get_time_greeting():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12: return "Good morning"
    elif 12 <= hour < 18: return "Good afternoon"
    else: return "Good evening"

def jarvis_logic(ui):
    global is_initialized
    is_initialized = True
    
    ui.start_btn.configure(state="disabled", text="OS ACTIVE")
    ui.terminal_log("INITIATING SECURITY PROTOCOLS...")
    ui.update_status("[ SCANNING ]", "#ffcc00")
    
    auth_result = verify_user()
    is_authorized = False

    if auth_result == "Authorized":
        is_authorized = True
        ui.terminal_log("BIOMETRIC MATCH CONFIRMED.")
    else:
        ui.terminal_log("BIOMETRICS FAILED. CHALLENGING PASSCODE...")
        ui.update_status("[ CHALLENGE ]", "#ffcc00")
        speak(f"Security alert. Biometric scan failed. {USER_NAME}, please provide manual override.")
        
        vocal_input = listen()
        manual_input = ui.pass_entry.get()

        if PASSCODE in vocal_input.lower() or manual_input == PASSCODE:
            is_authorized = True
            ui.terminal_log("OVERRIDE ACCEPTED. IDENTITY VERIFIED.")
            ui.pass_entry.delete(0, 'end')
        else:
            ui.terminal_log("ACCESS DENIED. SYSTEM LOCKED.")
            ui.update_status("[ LOCKED ]", "#ff3333")
            speak("Invalid credentials. System is locking down.")
            time.sleep(2)
            sys.exit()

    if is_authorized:
        ui.update_status("[ ACTIVE ]", "#00fbff")
        ui.terminal_log(f"AUTHORIZED USER: {USER_NAME}")
        
        greeting = f"{get_time_greeting()}, {USER_NAME}. {get_random_status()}"
        speak(greeting)
        ui.terminal_log("ALL SYSTEMS ONLINE. STANDING BY.")

    while True:
        ui.update_status("[ ACTIVE ]", "#00fbff")
        
        if wait_for_wake_word():
            ui.update_status("[ LISTENING ]", "#ff00ff")
            ui.terminal_log("Wake word detected.")
            
            speak("Ready.")
            query = listen()
            
            if not query:
                continue

            ui.terminal_log(f"USER: {query}")
            ui.update_status("[ PROCESSING ]", "#ffff00")

            response = ""

            if any(k in query for k in ["research", "search", "who is", "what is"]):
                ui.terminal_log("AGENT: Launching web research...")
                topic = query.replace("research", "").replace("search", "").strip()
                response = research_topic(topic)
            
            elif any(k in query for k in ["look", "see", "identify", "what is this"]):
                ui.terminal_log("VISION: Analyzing camera feed...")
                vision_context = capture_and_analyze()
                ui.terminal_log(f"VISION: {vision_context}")
                response = chat_with_ai(query, vision_context)
            
            else:
                ui.terminal_log("BRAIN: Processing via Llama...")
                response = chat_with_ai(query)

            ui.terminal_log(f"JARVIS RAW: {response}")
            
            command_feedback = execute_command(response)
            
            if command_feedback:
                ui.terminal_log(f"ACTION: {command_feedback}")
                speak(command_feedback)
            else:
                speak(response)

def start_program():
    """Triggered by HUD button"""
    if not is_initialized:
        logic_thread = threading.Thread(target=jarvis_logic, args=(app,), daemon=True)
        logic_thread.start()

if __name__ == "__main__":
    app = JarvisUI(start_program)
    app.bind("<Escape>", lambda e: sys.exit())
    try:
        app.mainloop()
    except KeyboardInterrupt:
        sys.exit()