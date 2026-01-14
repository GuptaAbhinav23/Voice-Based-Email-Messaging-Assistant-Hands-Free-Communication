import cv2
import streamlit as st
import time
import os

def capture_face_image(save_path="faces", filename="face.jpg", timeout=10):
    os.makedirs(save_path, exist_ok=True)
    image_path = os.path.join(save_path, filename)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    start_time = time.time()

    st.info("📷 Look straight at the camera")
    frame_placeholder = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            raise Exception("Camera not accessible")

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(rgb, channels="RGB", use_container_width=True)

        # Save after stable frame
        if time.time() - start_time > 3:
            cv2.imwrite(image_path, frame)
            cap.release()
            frame_placeholder.empty()
            st.success("✅ Face image captured")
            return image_path

        if time.time() - start_time > timeout:
            cap.release()
            frame_placeholder.empty()
            raise Exception("❌ Face capture timeout")
