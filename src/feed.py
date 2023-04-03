import base64

import cv2

from src.facial_analysis import add_facial_analysis

camera = cv2.VideoCapture(0)


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
