# register_face được sử dụng dựa vào 2 tệp(SQL,train) với các bước:
# Step 1: nhập thông tin người dùng(ID,name) bằng SQL với insertOrUpdate function
# Step 2: Dùng web cam để lấy ảnh của user và sử dụng haarcascade để có thể chụp đúng kích thước khuôn mặt yêu cầu để train
# Step 3: Sử dụng getImagesWithLabels function trong tệp train.py để train và lưu tệp ảnh thành xml

import cv2, os,glob
import sqlite3
import numpy as np
from PIL import Image
from train import getImagesWithLabels
from SQL import insertOrUpdate,delete_record_by_id
if not os.path.exists('dataset1'):
                os.makedirs('dataset1')
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
def Id_synx(a):
    while True:
        try:
            Id = int(input(a))
            return Id
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
def del_id(Id):
    folder_path = 'dataset1/'
    file_pattern = f'User.{Id}.*.jpg'
    files_to_delete = glob.glob(os.path.join(folder_path, file_pattern))
    for file_path in files_to_delete:
        os.remove(file_path)
    print(f"Deleted: {Id}")
def quest():
    print('Have you finished taking photos yet?')
    ans = input('Please enter Y/N/C: ').upper()
    return ans
def webcam(Id,name):
    cap = cv2.VideoCapture(0)
    count = 0
    insertOrUpdate(Id,name)
    while True:
        
        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y),(x+w,y+h), (0,255,0),2)
            if cv2.waitKey(1) == ord('c'):
                face = gray[y:y+h, x:x+w]
                resized_face = cv2.resize(face, (64, 64)) 
                cv2.imwrite('dataset1/User.' + str(Id) + '.' + str(count) + '.jpg',resized_face)
                count +=1 
        frame_height, frame_width = frame.shape[:2]
        (text_width, text_height),_ = cv2.getTextSize(str(count),cv2.FONT_HERSHEY_COMPLEX, 1,2)
        x = frame_width - text_width - 10 
        y = text_height + 10  
        cv2.putText(frame, str(count), (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 127),2)
        cv2.imshow('Webcam', frame)
        if count > 35:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def make(Id):
    print('Have you finished taking photos yet?')
    while True:
        try:
            ans = input('Please enter Y/N/C: ').upper()
            if ans not in ('Y', 'N', 'C'):
                raise ValueError("Invalid input")
            else:
                if ans == 'Y':
                    if os.path.exists('dataset1/training.xml'):
                        os.remove('dataset1/training.xml')
                    faces, Ids = getImagesWithLabels('dataset1')
                    recognizer = cv2.face.LBPHFaceRecognizer_create()
                    recognizer.train(faces, np.array(Ids))
                    recognizer.save('dataset1/training.xml')
                elif ans =='N':
                    del_id(Id)  
                    delete_record_by_id(Id)
                    ID = Id_synx("Please enter the Id: ")
                    name = input("Please enter your name: ")     
                    webcam(ID,name)
                    make(ID)
                elif ans == 'C':
                    del_id(Id)
                    delete_record_by_id(Id)
                    quit()
                break  
        except ValueError as e:
            print(e)
            print("Invalid input. Please enter Y/N/C.")

Id = Id_synx("Please enter the Id: ")
Name = input("Please enter your name: ")     
webcam(Id,Name)
make(Id)
