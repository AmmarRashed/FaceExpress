from deepface import DeepFace


def analyze_face(img):
    try:
        obj = DeepFace.analyze(img, actions=("emotion"))
    except ValueError:
        return None, None
    else:
        data = obj[0]  # assuming there is only one face
        return data["region"], data["emotion"]
