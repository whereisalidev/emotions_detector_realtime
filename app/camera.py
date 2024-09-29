import cv2
import threading
from deepface import DeepFace

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            raise IOError("Cannot open webcam")
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()
    
    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 128, 0), 2)
            face_region = image[y:y + h, x:x + w]

            try:
                analyze = DeepFace.analyze(face_region, actions=['emotion'], enforce_detection=False)
                emotions = analyze[0]['emotion']  

                dominant_emotion = max(emotions, key=emotions.get)
                confidence = emotions[dominant_emotion]

                cv2.putText(image, f"{dominant_emotion}: {confidence:.2f}%", (x, y - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (224, 77, 176), 2)

            except Exception as e:
                print('No face or error analyzing face:', e)

        ret, jpeg = cv2.imencode('.jpg', image)

        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
