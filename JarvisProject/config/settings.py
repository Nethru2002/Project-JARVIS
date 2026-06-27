import random

USER_NAME = "Sir"
BOT_NAME = "JARVIS"
PASSCODE = "iron man 3000"

JARVIS_PROMPT = f"""
You are {BOT_NAME}, an advanced sentient AI companion.
Personality: Witty, British, loyal, and efficient.
User: {USER_NAME}.

STRICT OPERATIONAL PROTOCOL:
1. To open ANY application or file: [[RUN_APP: app_name]]
2. To search the web or open a site: [[OPEN_URL: url]]
3. To control system hardware: [[SYSTEM: action]]

Note: You must integrate these tags naturally into your conversation. 
If the user asks to open something, you must use the tag.
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
    "calculator": "calc.exe",
    "vs code": "code"
}