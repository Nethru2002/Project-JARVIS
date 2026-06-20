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
    """Calculates Morning, Afternoon, or Evening based on system clock"""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def jarvis_logic(ui):
    """Handles the high-level logic in a background thread"""
    global is_initialized
    is_initialized = True
    
    ui.start_btn.configure(state="disabled", text="SYSTEMS ACTIVE")
    ui.terminal_log("INITIATING A.R.C.H.E.R. SECURITY PROTOCOLS...")
    ui.status_label.configure(text="[ SCANNING ]", text_color="#ffcc00")
    
    auth_result = verify_user() 
    is_authorized = False

    if auth_result == "Authorized":
        is_authorized = True
        ui.terminal_log("BIOMETRIC MATCH FOUND. IDENTITY CONFIRMED.")
    else:
        ui.terminal_log("BIOMETRICS UNRECOGNIZED. CHALLENGING VOCAL PASSCODE...")
        ui.status_label.configure(text="[ CHALLENGE ]", text_color="#ffcc00")
        
        speak(f"Security alert. Biometric verification failed. {USER_NAME}, please provide your override passcode.")
        
        vocal_input = listen()
        manual_input = ui.pass_entry.get()

        if PASSCODE in vocal_input.lower() or manual_input == PASSCODE:
            is_authorized = True
            ui.terminal_log("MANUAL OVERRIDE ACCEPTED. ACCESS GRANTED.")
            ui.pass_entry.delete(0, 'end') 
        else:
            ui.terminal_log("CRITICAL ERROR: UNAUTHORIZED ACCESS ATTEMPT.")
            ui.status_label.configure(text="[ LOCKED ]", text_color="#ff3333")
            speak("Invalid credentials. System is locking down. Goodbye.")
            time.sleep(2)
            sys.exit()

    if is_authorized:
        ui.status_label.configure(text="[ ACTIVE ]", text_color="#00fbff")
        ui.terminal_log(f"AUTHORIZED USER: {USER_NAME}")
        
        time_greet = get_time_greeting()
        status_update = get_random_status()
        
        speak(f"{time_greet}, {USER_NAME}. {status_update}")
        ui.terminal_log("ALL NEURAL NETWORKS ONLINE AND SYNCHRONIZED.")

    while True:
        ui.status_label.configure(text="[ MONITORING ]", text_color="#007a7a")
        
        if wait_for_wake_word():
            ui.status_label.configure(text="[ LISTENING ]", text_color="#ff00ff")
            ui.terminal_log("Wake word detected.")
            
            speak("Online. What is your command?")
            query = listen()
            
            if not query or query == "":
                ui.status_label.configure(text="[ ACTIVE ]", text_color="#00fbff")
                continue

            ui.terminal_log(f"INPUT: {query}")
            ui.status_label.configure(text="[ THINKING ]", text_color="#ffff00")

            if any(k in query for k in ["research", "search", "who is", "tell me about"]):
                ui.terminal_log("AGENT: Launching web research sequence...")
                topic = query.replace("research", "").replace("search", "").strip()
                response = research_topic(topic)
            
            elif any(k in query for k in ["look", "see", "identify", "what is this"]):
                ui.terminal_log("VISION: Analyzing optic feed...")
                vision_context = capture_and_analyze()
                ui.terminal_log(f"VISION ANALYTICS: {vision_context}")
                response = chat_with_ai(query, vision_context)
            
            else:
                ui.terminal_log("COGNITION: Processing query...")
                response = chat_with_ai(query)

            ui.terminal_log(f"JARVIS: {response[:50]}...")
            
            sys_feedback = execute_command(response)
            if sys_feedback:
                speak(sys_feedback)
            else:
                speak(response)

            ui.status_label.configure(text="[ ACTIVE ]", text_color="#00fbff")

def start_program():
    """Triggered by GUI button. Starts logic thread only once."""
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