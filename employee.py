
#code to get images of employee to train

import cv2
import os

video=cv2.VideoCapture(0)
#create an object for cascade classifier
face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# faces_data=[]
name=input("Enter your name : ")
path=os.path.join("DB",name)
os.makedirs(path)
i=0
img_id=0
while True:
    ret,frame=video.read()
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #conver the bgr image to gray for better processing
    faces=face_cascade.detectMultiScale(gray,1.3,5)
    
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),color=(0,0,255),thickness=1) #draw a rectangle around the detected face
        crop_image=frame[y:y+h,x:x+w] #crop the image inside the rectangle
        if int(img_id)<=100 and i%10==0:  #images after every 10 frames till 100 is taken so that we can get time to capture several expression of the face
            img_path=path+"/"+str(img_id)+".jpg"
            cv2.imwrite(img_path,crop_image)
            img_id+=1
        i=i+1
        cv2.putText(frame,str(img_id),org=(50,50),fontFace=cv2.FONT_HERSHEY_COMPLEX,color=(255,0,0),fontScale=1,thickness=2)
    cv2.imshow("IMAGE",frame)
    k=cv2.waitKey(1)
    if k==ord("q") or int(img_id)==100 :
        break
video.release()
cv2.destroyAllWindows()




