import cv2
import numpy as np
import face_recognition
from datetime import datetime
import os
path='images'
images=[]
classNames=[]
myList=os.listdir(path)
print(myList)

for cls in myList:
    curImg=cv2.imread(f'{path}/{cls}')
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])
print(classNames)
#Function to calculate encodings
def findEncoding(images):
    encodeList=[]
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Covert to RGB
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeListKnown=findEncoding(images)
print('Encoding complete')
#Initializing web cam to match image
cap= cv2.VideoCapture(0)
def marattendance(n):
    with open('attendnece.csv','r+') as f: # Reading a data
        data=f.readlines()
        name=[]
        for i in data:
            e=i.split(',')
            name.append(e[0]) # name
        if (n not in name):
            time=datetime.now()
            datestr= time.strftime('%H:%M:%S')
            f.writelines(f'\n{n},{datestr}')
while True:
    success,img = cap.read()
    imgSmall = cv2.resize(img,(0,0),None,0.25,0.25)#Reduciing the size to 1/4 th as we are doing it in real time makes it faster process
    imgSmall = cv2.cvtColor(imgSmall, cv2.COLOR_BGR2RGB)  # Covert to RGB
    # A frame can have multiple faces
    facesCurrFrame = face_recognition.face_locations(imgSmall)
    encodeCurr = face_recognition.face_encodings(imgSmall,facesCurrFrame)
    #Looping through the current faces in list and then matching it with all the images in folder
    for encodFace,faceLoc in zip(encodeCurr,facesCurrFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodFace)
        print(matches)
        faceDis=face_recognition.face_distance(encodeListKnown,encodFace) # Will give us three values as 3 images the lowest distance will be the best match
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1,x2,y2,x1=faceLoc
            y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4 # This is to again get to noermal size
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)#coordinates , color , thickness
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
            marattendance(name)
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)
