import cv2
import os
path='images'
print("Enter Name")
name=input()
print("Hit spacebar to take a photo")
cam=cv2.VideoCapture(0)
while True:
    ret,frame=cam.read()
    if not ret :
        print("fail to grab frame")
        break
    cv2.imshow("test",frame)
    k=cv2.waitKey(1)
    if k%256 == 27:
        print("Esc hit, closing the app")
    elif k%256 == 32:
        img_name= name+".jpg"
        cv2.imwrite(os.path.join(path,img_name),frame)
        print("Screenshot taken")
        break
cv2.namedWindow("Registration")
cam.release()
