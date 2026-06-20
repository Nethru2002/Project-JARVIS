import speech_recognition as sr

def wait_for_wake_word():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=3)
            text = r.recognize_google(audio).lower()
            return "jarvis" in text
        except:
            return False