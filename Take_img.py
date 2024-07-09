import cv2
import os
import numpy as np
from train import getImagesWithLabels

if not os.path.exists('dataset1'):
                os.makedirs('dataset1')
if os.path.exists('dataset1/training.xml'):
    os.remove('dataset1/training.xml')

cascPath = 'haarcascade_frontalface_default.xml'
detc = cv2.CascadeClassifier(cascPath)

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()
cap = cv2.VideoCapture(0)
count = 0
id = input('Enter your ID: ')

if not cap.isOpened():
    print("Không thể mở webcam")
    exit()

while True:

    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detc.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y),(x+w,y+h), (0,255,0),2)
        if cv2.waitKey(1) == ord('c'):
            face = gray[y:y+h, x:x+w]
            resized_face = cv2.resize(face, (64, 64)) 
            cv2.imwrite('dataset1/User.' + str(id) + '.' + str(count) + '.jpg',resized_face)
            count +=1

    cv2.imshow('Webcam training', frame)
    if count > 35:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
faces, Ids = getImagesWithLabels('dataset1')
recognizer.train(faces, np.array(Ids))
recognizer.save('dataset1/training.xml')
