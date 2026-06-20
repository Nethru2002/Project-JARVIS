import webbrowser
import os
import pyautogui
import psutil
from config.settings import APP_PATHS

def execute_command(ai_response):
    if "[[OPEN_URL:" in ai_response:
        url = ai_response.split("[[OPEN_URL:")[1].split("]]")[0].strip()
        webbrowser.open(url)
        
    elif "[[RUN_APP:" in ai_response:
        app = ai_response.split("[[RUN_APP:")[1].split("]]")[0].strip().lower()
        if app in APP_PATHS:
            os.startfile(APP_PATHS[app])
            
    elif "[[SYSTEM:" in ai_response:
        action = ai_response.split("[[SYSTEM:")[1].split("]]")[0].strip()
        if "screenshot" in action:
            pyautogui.screenshot("jarvis_snap.png")
        elif "volume up" in action:
            pyautogui.press("volumeup", presses=5)
        elif "battery" in action:
            battery = psutil.sensors_battery()
            return f"Sir, the battery is at {battery.percent}%"
    return None