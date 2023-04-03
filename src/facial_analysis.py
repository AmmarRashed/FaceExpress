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


def add_facial_analysis(frame):
    region, emotion = analyze_face(frame)
    if region is not None:
        frame = draw_face_box(frame, region)
    return frame, emotion
