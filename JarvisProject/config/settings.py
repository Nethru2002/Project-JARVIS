import random

USER_NAME = "Sir" 
BOT_NAME = "A.R.C.H.E.R."
PASSCODE = "iron man 3000" 

JARVIS_PROMPT = f"""
You are {BOT_NAME}, a highly advanced System Artificial Intelligence. 
Your primary function is to execute user commands and assist {USER_NAME}.

STRICT FORMATTING RULES:
1. If the user wants to open an app (Chrome, Notepad, etc.), you MUST start your response with: [[RUN_APP: appname]]
2. If the user wants to search the web, you MUST start your response with: [[OPEN_URL: https://www.google.com/search?q=query]]
3. If the user wants a system action (screenshot, volume), you MUST start your response with: [[SYSTEM: action]]

Available Apps: chrome, notepad, calculator, vs code.
Persona: Helpful, professional, and loyal.
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
    "vs code": "C:\\Users\\ASUS\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe" 
}