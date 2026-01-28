from database.db import get_db
from biometric.capture_face import capture_face_image
from biometric.verify_face import verify_faces

def login_user(username: str) -> bool:
    """
    Verifies a user using face recognition.
    Returns True if verified, else False.
    """

    if not username:
        return False

    conn = get_db()
    c = conn.cursor()

    # Fetch stored face image path
    c.execute(
        "SELECT face_path FROM users WHERE username=?",
        (username,)
    )
    row = c.fetchone()
    conn.close()

    if not row:
        return False

    db_face_image = row[0]  # path stored in DB

    # Capture live face
    live_face_path = capture_face_image(
        filename=f"live_{username}.jpg"
    )

    # Verify faces
    return verify_faces(db_face_image, live_face_path)

