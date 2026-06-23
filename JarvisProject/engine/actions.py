import os
import webbrowser
import pyautogui
from config.settings import APP_PATHS

def execute_command(ai_response):
    response_lower = ai_response.lower()
    
    if "[[" in ai_response and "]]" in ai_response:
        if "RUN_APP" in ai_response:
            app = ai_response.split("RUN_APP:")[1].split("]]")[0].strip().lower()
            return open_app_logic(app)
        
        if "OPEN_URL" in ai_response:
            url = ai_response.split("OPEN_URL:")[1].split("]]")[0].strip()
            webbrowser.open(url)
            return "Accessing the requested URL."

    if "open" in response_lower:
        for app in APP_PATHS:
            if app in response_lower:
                return open_app_logic(app)
                
    if "google" in response_lower or "search" in response_lower:
        search_query = response_lower.replace("search", "").replace("google", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
        return f"Searching for {search_query}."

    if "screenshot" in response_lower or "snap" in response_lower:
        pyautogui.screenshot("jarvis_snap.png")
        return "Screenshot captured, sir."

    return None

def open_app_logic(app_name):
    """Internal helper to launch apps"""
    if app_name in APP_PATHS:
        try:
            os.startfile(APP_PATHS[app_name])
            return f"Initializing {app_name}."
        except:
            return f"System failed to launch {app_name}. Check file path."
    return f"{app_name} is not in my database."