# import cv2
# import streamlit as st
# import time
# import os

# def capture_face_image(save_path="faces", filename="face.jpg", timeout=10):
#     os.makedirs(save_path, exist_ok=True)
#     image_path = os.path.join(save_path, filename)

#     cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     start_time = time.time()

#     st.info("📷 Look straight at the camera")
#     frame_placeholder = st.empty()

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             cap.release()
#             raise Exception("Camera not accessible")

#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         frame_placeholder.image(rgb, channels="RGB", use_container_width=True)

#         # Save after stable frame
#         if time.time() - start_time > 3:
#             cv2.imwrite(image_path, frame)
#             cap.release()
#             frame_placeholder.empty()
#             st.success("✅ Face image captured")
#             return image_path

#         if time.time() - start_time > timeout:
#             cap.release()
#             frame_placeholder.empty()
#             raise Exception("❌ Face capture timeout")


import cv2
import os
import time

def capture_face_image(save_path="faces", filename="face.jpg", timeout=10):
    os.makedirs(save_path, exist_ok=True)
    image_path = os.path.join(save_path, filename)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    start_time = time.time()

    if not cap.isOpened():
        raise Exception("Camera not accessible")

    print("📷 Capturing face... Look at the camera")

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            raise Exception("Failed to read from camera")

        cv2.imshow("Face Capture - Press SPACE to capture", frame)

        # Auto capture after 3 seconds
        if time.time() - start_time > 3:
            cv2.imwrite(image_path, frame)
            break

        # Manual capture with SPACE key
        if cv2.waitKey(1) & 0xFF == 32:
            cv2.imwrite(image_path, frame)
            break

        if time.time() - start_time > timeout:
            cap.release()
            cv2.destroyAllWindows()
            raise Exception("Face capture timeout")

    cap.release()
    cv2.destroyAllWindows()

    print("✅ Face image saved:", image_path)
    return image_path
