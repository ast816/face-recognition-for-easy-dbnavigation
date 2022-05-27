import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pyodbc
import time
import pickle
from imutils import paths
import argparse as args

server = 'asthasql.database.windows.net'
database = 'sql_facerecog'
username = 'azureadmin'
password = 'asthaface10_'   
driver= '{ODBC Driver 17 for SQL Server}'

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

ap = args.ArgumentParser()


PIK = "pickle.dat"


# append all images in image list and names in classNames
path = 'Face-Recognition-Attendance-Projects\Training_images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

#encode all images and save it in encodelist
def findEncodings(images):
    encodeList = []

   
    for img in images:
    
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

#show details wrt to name value in azure database
def showdb(name):
   
    cursor.execute("SELECT*FROM DETAILS WHERE Name =?",name)

   
    for row in cursor:
        print(row)

#Complete Encoding
encodeListKnown = findEncodings(images)
print('Encoding Complete')

# serialising encodings
print(" serializing encodings...")
data = {"encodings": encodeListKnown, "names": classNames}
f = open(PIK, "wb")
f.write(pickle.dumps(data))
f.close()
#switch on webcam and capture image
cap = cv2.VideoCapture(0)

#cap is read and stored in img
t_end = time.time() + 25
while time.time() < t_end:
    success, img = cap.read()

#resize and convertcolor
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#boundary captured face and encode it
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

#match encoded face with encodinglistKnown and check matches
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

#take the minium faceid number
        matchIndex = np.argmin(faceDis)

#check the name of person that matches the encoding with true match result and least faceid distance
        if matches[matchIndex]:
            name = classNames[matchIndex]

#show db function called with name as parameter
            showdb(name)
            
 #place rectangle on face
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
   
#show webcam 
    cv2.imshow('Webcam', img)    
    cv2.waitKey(1) 

#destroy all windows
cv2.destroyWindow('Webcam')