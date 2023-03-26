import base64

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


def encode_frame(frame):
    ret, buffer = cv2.imencode('.jpg', frame)
    frame_str = base64.b64encode(buffer).decode('utf-8')
    return frame_str


class FrameGenerator(object):
    def __init__(self, analyze_face=True):
        self.analyze_face = analyze_face

    def gen_frames(self):
        while True:
            success, frame = camera.read()
            if not success:
                continue
            else:
                data = {}
                if self.analyze_face:
                    frame, emotions = add_facial_analysis(frame)
                    data["emotions"] = emotions
                data["frame"] = encode_frame(frame)
                yield data
