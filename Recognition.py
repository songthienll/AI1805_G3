import cv2
from PIL import Image
from SQL import getProfile

face_cascade = cv2.CascadeClassifier( 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('D:/CPV301/Do my self/dataset1/training.xml')

threshold = 140
count = 0 
cap = cv2.VideoCapture(0)

tracker = None
ret, frame = cap.read()
recognized = False

while ret:
    if not recognized:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
        
        for (x, y, w, h) in faces:
            frame_height, frame_width = frame.shape[:2]
            (text_width, text_height),_ = cv2.getTextSize("DETECTING",cv2.FONT_HERSHEY_COMPLEX, 1,2)
            a = frame_width - text_width - 10 
            b = text_height + 10  
            cv2.putText(frame, "DETECTING", (a, b), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255),2)
            roi_gray = gray[y:y+h, x:x+w]
            id, conf = recognizer.predict(roi_gray)
            profile=getProfile(id)
            if conf < threshold:
                if id == profile[0]:
                    name = profile[1]
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)     
                    cv2.putText(frame, "Name : "+str(name), (x,y-5),cv2.FONT_HERSHEY_COMPLEX, 1,(0,255,127),2)
                else:
                    name = 'Unknown'
                    cv2.putText(frame, "Name : "+str(name), (x,y-5),cv2.FONT_HERSHEY_COMPLEX, 1,(0,255,127),2)
            else:
                    name = 'Unknown'
                    cv2.putText(frame, "Name : "+str(name), (x,y-5),cv2.FONT_HERSHEY_COMPLEX, 1,(0,255,127),2)

            tracker = cv2.TrackerKCF_create()
            tracker.init(frame, (x, y, w, h))
            recognized = True
            break
    else:
        ret, bbox = tracker.update(frame)        
        if ret:
            frame_height, frame_width = frame.shape[:2]
            (text_width, text_height),_ = cv2.getTextSize("TRACKING",cv2.FONT_HERSHEY_COMPLEX, 1,2)
            a = frame_width - text_width - 10 
            b = text_height + 10  
            cv2.putText(frame, "TRACKING", (a, b), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 127),2)
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
            cv2.putText(frame, "Name : "+str(name),(int(bbox[0]), int(bbox[1])-5),cv2.FONT_HERSHEY_COMPLEX, 1,(0,255,127),2)
        else:
            recognized = False  


    cv2.imshow('Webcam', frame)
    ret, frame = cap.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



