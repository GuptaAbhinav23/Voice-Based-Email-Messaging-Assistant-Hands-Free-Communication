# from deepface import DeepFace
# import os

# def verify_faces(db_image_path, live_image_path):

#     # Ensure DB image exists
#     if not os.path.exists(db_image_path):
#         print("DB image missing:", db_image_path)
#         return False

#     # Ensure live image exists
#     if not os.path.exists(live_image_path):
#         print("Live image missing")
#         return False

#     result = DeepFace.verify(
#         img1_path=db_image_path,      
#         img2_path=live_image_path,    
#         model_name="ArcFace",
#         detector_backend="retinaface",
#         enforce_detection=False
#     )

#     return result["verified"]



from deepface import DeepFace
import os

def verify_faces(db_image_path, live_image_path):
    if not os.path.exists(db_image_path):
        print("❌ DB image missing:", db_image_path)
        return False

    if not os.path.exists(live_image_path):
        print("❌ Live image missing:", live_image_path)
        return False

    try:
        result = DeepFace.verify(
            img1_path=db_image_path,
            img2_path=live_image_path,
            model_name="ArcFace",
            detector_backend="opencv",   # 🔥 changed
            enforce_detection=False
        )

        print("🔍 Face match result:", result["verified"])
        return result["verified"]

    except Exception as e:
        print("❌ DeepFace verification error:", e)
        return False
