import streamlit as st
import cv2
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import pandas as pd
import numpy as np
import av
import os
from PIL import Image


def app():
    st.title('Test Model')
    st.header('Upload your Image and Test the Model ')

    image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    
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

    class VideoProcessor:
        def recv(self, frame):
            frm = frame.to_ndarray(format="bgr24")

            return av.VideoFrame.from_ndarray(frm, format='bgr24')

    webrtc_streamer(key="key", video_processor_factory=VideoProcessor, rtc_configuration=RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    ))
