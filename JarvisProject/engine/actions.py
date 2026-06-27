import os
import webbrowser
import pyautogui
import subprocess
import time
import ctypes
from config.settings import APP_PATHS

try:
    import win32gui
    import win32con
except ImportError:
    win32gui = None

def execute_command(ai_response):
    res_lower = ai_response.lower()

    if "[[" in ai_response and "]]" in ai_response:
        try:
            tag_content = ai_response.split("[[")[1].split("]]")[0]
            command_type, value = tag_content.split(":", 1)
            value = value.strip().lower()

            if "RUN_APP" in command_type:
                return smart_launcher(value)
            elif "OPEN_URL" in command_type:
                webbrowser.open(value)
                return "Accessing network resource."
            elif "SYSTEM" in command_type:
                return system_control(value)
        except:
            pass

    if "open" in res_lower or "launch" in res_lower:
        for app in APP_PATHS:
            if app in res_lower:
                return smart_launcher(app)
        
        words = res_lower.split()
        try:
            idx = words.index("open")
            if idx + 1 < len(words):
                return smart_launcher(words[idx+1])
        except:
            pass

    return None

def smart_launcher(app_name):
    if win32gui:
        def window_enum_handler(hwnd, resultList):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd).lower()
                if app_name in title:
                    resultList.append(hwnd)
        
        hwnds = []
        win32gui.EnumWindows(window_enum_handler, hwnds)
        
        if hwnds:
            hwnd = hwnds[0]
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return f"Switching to active {app_name} instance."

    if app_name in APP_PATHS:
        try:
            os.startfile(APP_PATHS[app_name])
            return f"Launching {app_name}."
        except:
            pass
    
    try:
        subprocess.Popen(f"start {app_name}", shell=True)
        return f"Executing system shell command for {app_name}."
    except:
        return f"Unable to locate {app_name}."

def system_control(action):
    if "screenshot" in action or "snap" in action:
        fname = f"snapshot_{int(time.time())}.png"
        pyautogui.screenshot(fname)
        return f"Capture saved as {fname}."
    elif "volume up" in action:
        pyautogui.press("volumeup", presses=5)
        return "Audio increased."
    elif "volume down" in action:
        pyautogui.press("volumedown", presses=5)
        return "Audio decreased."
    elif "fullscreen" in action:
        pyautogui.press("f11")
        return "Toggling display mode."
    return "Command executed."