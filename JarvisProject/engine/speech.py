import whisper
import edge_tts
import pygame
import asyncio
import os
import time
import re
import torch
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)

VOICE = "en-GB-RyanNeural"
ACTIVE_MIC_INDEX = None

def choose_best_microphone():
    global ACTIVE_MIC_INDEX
    devices = sd.query_devices()
    input_devices = [i for i, d in enumerate(devices) if d['max_input_channels'] > 0]
    
    best_idx = sd.default.device[0]
    max_rms = 0
    
    for idx in input_devices:
        try:
            with sd.InputStream(device=idx, channels=1, samplerate=16000) as stream:
                data, _ = stream.read(1024)
                rms = np.sqrt(np.mean(data**2))
                if rms > max_rms:
                    max_rms = rms
                    best_idx = idx
        except:
            continue
    
    ACTIVE_MIC_INDEX = best_idx
    return best_idx

def speak(text):
    clean_text = re.sub(r'\[\[.*?\]\]', '', text).strip()
    if not clean_text:
        clean_text = "Standard protocol executed, sir."

    async def _speak():
        filename = f"speech_{int(time.time() * 1000)}.mp3"
        try:
            communicate = edge_tts.Communicate(clean_text, VOICE)
            await communicate.save(filename)
            
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
            
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.quit()
        except:
            pass
        finally:
            try:
                if os.path.exists(filename):
                    os.remove(filename)
            except:
                pass

    asyncio.run(_speak())

def listen():
    fs = 16000
    duration = 5 
    
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, device=ACTIVE_MIC_INDEX)
        sd.wait()
        
        wav_path = "temp_vocal.wav"
        wav.write(wav_path, fs, (recording * 32768).astype(np.int16))
        
        result = model.transcribe(wav_path, fp16=False)
        query = result["text"].strip().lower()
        
        if os.path.exists(wav_path):
            os.remove(wav_path)
        return query
    except:
        return ""