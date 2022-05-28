from re import M
import streamlit as st
import cv2
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import pandas as pd
import numpy as np
import av
import os
from PIL import Image
import pickle
import argparse
import face_recognition


def app():
    st.title('Test Model')
    st.header('Upload your Image and Test the Model ')

    image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    
    # Load face encodings
    # with open('dataset_faces.dat','rb') as f:
    #     encoding=pickle.load(f)
    #     names=pickle.load(f)
        
    




    @st.cache
    def load_image(image_file):
        img=Image.open(image_file)
        return img

    if image_file is not None:
        file_details = {"FileName": image_file.name,
                        "FileType": image_file.type}
        
        img = load_image(image_file)
        st.image(img,width=100)
        with open( os.path.join("Training_images",image_file.name), "wb") as f:
            f.write(image_file.getbuffer())
        st.success("Saved File")
     
    def processing(frame):
        
        while True:
            success, img = frame.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            #boundary captured face and encode it
            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
#match encoded face with encodinglistKnown and check matches
            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodings, encodeFace)
                faceDis = face_recognition.face_distance(encodings, encodeFace)
             

#take the minium faceid number
                matchIndex = np.argmin(faceDis)

#check the name of person that matches the encoding with true match result and least faceid distance
                if matches[matchIndex]:
                    name = names[matchIndex]
            
#show db function called with name as parameter
            # showdb(name)
            
 #place rectangle on face
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                return frame
            
   





        
    class VideoProcessor:
        def recv(self, frame):
            frm = frame.to_ndarray(format="bgr24")
            processing(frame)
            

            return av.VideoFrame.from_ndarray(frm, format='bgr24')

    webrtc_streamer(key="key", video_processor_factory=VideoProcessor, rtc_configuration=RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    ))

   