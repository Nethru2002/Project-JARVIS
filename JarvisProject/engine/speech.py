import speech_recognition as sr
import edge_tts
import pygame
import asyncio
import os
import time
import re

VOICE = "en-GB-RyanNeural" 

def speak(text):
    """Clean text of tags and speak using a unique file to prevent permission locks"""
    clean_text = re.sub(r'\[\[.*?\]\]', '', text).strip()
    
    if not clean_text:
        clean_text = "Task completed, sir."

    async def _speak():
        filename = f"voice_{int(time.time() * 1000)}.mp3"
        
        try:
            communicate = edge_tts.Communicate(clean_text, VOICE)
            await communicate.save(filename)
            
            pygame.mixer.init()
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
                
            pygame.mixer.music.stop()
            pygame.mixer.music.unload() 
            pygame.mixer.quit()
        except Exception as e:
            print(f"Speech Error: {e}")
        finally:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except:
                pass

    asyncio.run(_speak())

def listen():
    """Captures voice and returns string"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=4)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            return query.lower()
        except:
            return ""