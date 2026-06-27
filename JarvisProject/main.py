import threading
import sys
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

def jarvis_logic(ui):
    global is_initialized
    is_initialized = True
    
    ui.start_btn.configure(state="disabled", text="ONLINE")
    ui.terminal_log("LOADING GALAXY HUD CORE...")
    
    best_mic = choose_best_microphone()
    ui.terminal_log(f"HARDWARE: MIC {best_mic} ACTIVE")
    
    ui.update_status("[ SCANNING ]", "#ffcc00")
    if verify_user() != "Authorized":
        ui.update_status("[ CHALLENGE ]", "#ffcc00")
        speak("Biometric failure. Passcode required.")
        vocal_input = listen()
        if PASSCODE in vocal_input.lower() or ui.pass_entry.get() == PASSCODE:
            ui.terminal_log("MANUAL OVERRIDE ACCEPTED.")
        else:
            ui.update_status("[ LOCKED ]", "#ff0055")
            speak("Access denied.")
            sys.exit()

    ui.update_status("[ ACTIVE ]", "#00fbff")
    speak(f"Hello {USER_NAME}. {get_random_status()}")

    while True:
        ui.update_status("[ ACTIVE ]", "#00fbff")
        if wait_for_wake_word():
            ui.update_status("[ LISTENING ]", "#ff00ff")
            speak("Ready.")
            query = listen()
            if not query: continue

            ui.terminal_log(f"USER: {query}")
            ui.update_status("[ PROCESSING ]", "#5e17eb")

            if "research" in query:
                response = research_topic(query)
            elif "look" in query or "see" in query:
                response = chat_with_ai(query, capture_and_analyze())
            else:
                response = chat_with_ai(query)

            action_feedback = execute_command(response)
            if action_feedback:
                ui.terminal_log(f"CMD: {action_feedback}")
                speak(action_feedback)
            else:
                speak(response)

if __name__ == "__main__":
    app = JarvisUI(lambda: threading.Thread(target=jarvis_logic, args=(app,), daemon=True).start())
    app.bind("<Escape>", lambda e: sys.exit())
    app.mainloop()