import cv2
import ollama
import os

def capture_and_analyze():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    if not ret:
        return "Sir, I cannot access the camera."
    
    img_path = "vision_temp.jpg"
    cv2.imwrite(img_path, frame)
    cam.release()

    try:
        with open(img_path, "rb") as img_file:
            response = ollama.generate(
                model='llava',
                prompt="Describe what you see in this image briefly and professionally.",
                images=[img_file.read()]
            )
        os.remove(img_path)
        return response['response']
    except Exception as e:
        return f"Vision error: {e}"