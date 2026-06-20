import random

USER_NAME = "Sir" 
BOT_NAME = "JARVIS"
PASSCODE = "iron man 3000"

JARVIS_PROMPT = f"""
You are {BOT_NAME}, a sophisticated AI. You are helpful, witty, and slightly sarcastic.
You have access to the user's laptop. 
- If asked to open an app, use [[RUN_APP: app_name]].
- If asked to search, use [[OPEN_URL: url]].
- If asked for system stats, use [[SYSTEM: action]].
Context: You are speaking to {USER_NAME}.
"""

def get_random_status():
    status_reports = [
        "All systems are functioning within normal parameters.",
        "Neural networks are synchronized and stable.",
        "I've optimized the background processes while you were away.",
        "Power levels are optimal. Ready for your command.",
        "Internet connection is stable. Global databases are accessible."
    ]
    return random.choice(status_reports)

APP_PATHS = {
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe"
}