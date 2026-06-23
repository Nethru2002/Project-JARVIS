import speech_recognition as sr

def wait_for_wake_word():
    r = sr.Recognizer()
    r.energy_threshold = 200 
    r.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.3)
        try:
            audio = r.listen(source, timeout=None, phrase_time_limit=3)
            text = r.recognize_google(audio).lower()
            print(f"DEBUG: Heard '{text}'")
            
            if "jarvis" in text or "hey" in text or "system" in text:
                return True
        except:
            return False
    return False