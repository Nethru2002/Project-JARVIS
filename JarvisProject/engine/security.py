import face_recognition
import cv2
import os

def verify_user():
    if not os.path.exists("me.jpg"):
        print("Error: 'me.jpg' not found.")
        return "No Reference Image"

    try:
        my_image = face_recognition.load_image_file("me.jpg")
        my_face_encoding = face_recognition.face_encodings(my_image)[0]

        video_capture = cv2.VideoCapture(0)
        for i in range(10): video_capture.read() 
        
        ret, frame = video_capture.read()
        video_capture.release()

        if not ret: return "Camera Error"

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            results = face_recognition.compare_faces([my_face_encoding], face_encoding, tolerance=0.6)
            if results[0]:
                return "Authorized"
                
        return "Failed"
    except Exception as e:
        print(f"Security Error: {e}")
        return "Error"