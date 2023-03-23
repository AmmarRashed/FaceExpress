import cv2

from utils.facial_analysis import analyze_face

camera = cv2.VideoCapture(0)


def draw_face_box(frame, region):
    x1, y1, w, h = region["x"], region["y"], region["w"], region["h"]
    x2, y2 = x1 + w, y1 + h
    return cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)


def add_facial_analysis(frame):
    region, emotion = analyze_face(frame)
    if region is not None:
        frame = draw_face_box(frame, region)
    return frame, emotion


def get_webcam_feed():
    while True:
        success, frame = camera.read()
        if not success:
            continue
        else:
            frame, emotion = add_facial_analysis(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'), emotion
