import speech_recognition as sr
import edge_tts
import pygame
import asyncio
import os
import time

VOICE = "en-GB-RyanNeural" 

def speak(text):
    """High-quality human-like speech with unique file handling to prevent locks"""
    async def _speak():
        filename = f"temp_voice_{int(time.time() * 1000)}.mp3"
        
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(filename)
        
        # Initialize mixer
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.music.stop()
            pygame.mixer.music.unload() 
        finally:
            pygame.mixer.quit()
            
            for _ in range(5):
                try:
                    if os.path.exists(filename):
                        os.remove(filename)
                    break
                except PermissionError:
                    time.sleep(0.2)

    asyncio.run(_speak())

def listen():
    """Listens for user voice input"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5) 
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        return query.lower()
    except:
        return ""