try:
    import sounddevice
    import whisper
    import scipy
    print("SUCCESS: All modules are installed and ready!")
except ImportError as e:
    print(f"FAILED: {e}")