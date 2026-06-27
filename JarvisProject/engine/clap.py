import numpy as np
import sounddevice as sd
import time

def listen_for_claps(callback):
    """Listens for a double-clap to trigger the assistant"""
    threshold = 0.3 
    cooldown = 0.5
    last_clap = 0
    
    def audio_callback(indata, frames, time_info, status):
        nonlocal last_clap
        volume_norm = np.linalg.norm(indata) * 10
        if volume_norm > threshold:
            now = time.time()
            if (now - last_clap) < cooldown and (now - last_clap) > 0.1:
                print(">>> DOUBLE CLAP DETECTED")
                callback()
            last_clap = now

    with sd.InputStream(callback=audio_callback):
        while True: sd.sleep(1000)