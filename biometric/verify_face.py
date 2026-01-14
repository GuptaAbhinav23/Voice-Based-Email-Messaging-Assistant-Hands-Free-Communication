from deepface import DeepFace
import os

def verify_faces(db_image_path, live_image_path):

    # Ensure DB image exists
    if not os.path.exists(db_image_path):
        print("DB image missing:", db_image_path)
        return False

    # Ensure live image exists
    if not os.path.exists(live_image_path):
        print("Live image missing")
        return False

    result = DeepFace.verify(
        img1_path=db_image_path,      
        img2_path=live_image_path,    
        model_name="ArcFace",
        detector_backend="retinaface",
        enforce_detection=False
    )

    return result["verified"]


