import cv2

from src.facial_analysis import add_facial_analysis
from src.utils import encode_frame


class FrameGenerator(object):
    def __init__(self, video_src, analyze_face=True):
        self.video_src = video_src
        self.video = cv2.VideoCapture(self.video_src)
        self.analyze_face = analyze_face

    def gen_frames(self):
        while True:
            success, frame = self.video.read()
            if not success:
                continue
            else:
                data = {}
                if self.analyze_face:
                    frame, face, emotions = add_facial_analysis(frame)
                    data["emotions"] = emotions
                    data["face"] = encode_frame(face)
                data["frame"] = encode_frame(frame)
                yield data
