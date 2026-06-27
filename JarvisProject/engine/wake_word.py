import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer

if not os.path.exists("model"):
    print("Please download the Vosk model and rename the folder to 'model'.")
    exit()

model = Model("model")
rec = KaldiRecognizer(model, 16000, '["jarvis", "hey", "system", "[unk]"]')

def wait_for_wake_word():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    print(">>> A.R.C.H.E.R. is monitoring the room...")

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "")
            if "jarvis" in text or "hey" in text:
                stream.stop_stream()
                stream.close()
                p.terminate()
                return True
    return False