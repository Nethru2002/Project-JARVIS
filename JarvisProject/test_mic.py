import speech_recognition as sr

def test():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(">>> Adjusting for background noise... Please be quiet.")
        r.adjust_for_ambient_noise(source, duration=2)
        print(">>> MICROPHONE ACTIVE. Say 'Hello Jarvis' now...")
        
        try:
            audio = r.listen(source, timeout=5)
            print(">>> Recognizing...")
            text = r.recognize_google(audio)
            print(f">>> SUCCESS! You said: '{text}'")
        except Exception as e:
            print(f">>> ERROR: {e}")

if __name__ == "__main__":
    test()