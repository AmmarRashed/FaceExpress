from deepface import DeepFace

from src.utils import draw_face_box


def analyze_face(img):
    try:
        obj = DeepFace.analyze(img, actions=("emotion"))
    except ValueError:
        return None, None
    else:
        data = obj[0]  # assuming there is only one face
        return data["region"], data["emotion"]


def add_facial_analysis(frame, crop_face=True):
    region, emotion = analyze_face(frame)
    face = None
    if region is not None:
        frame, face = draw_face_box(frame, region, crop=crop_face)
    return frame, face, emotion
