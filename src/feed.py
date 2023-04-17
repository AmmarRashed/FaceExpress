import cv2

from src.facial_analysis import analyze_face, detect_face
from src.utils import encode_frame
import imutils
from imutils.video import WebcamVideoStream, FileVideoStream


class FrameGenerator(object):
    def __init__(self, video_src, analyze_face=True):
        self.video_src = video_src
        self.video = WebcamVideoStream(0) if video_src == "0" else FileVideoStream(self.video_src)
        self.video.start()
        self.analyze_face = analyze_face

    def gen_frames(self):
        while True:
            frame = self.video.read()
            if frame is None:
                continue
            else:
                data = {"frame": encode_frame(frame)}
                face = detect_face(frame)
                if face is None:
                    yield data
                    continue
                data["face_img"] = encode_frame(face)
                if self.analyze_face:
                    analysis = analyze_face(face[:, :, ::-1])  # correct colors
                    data.update(analysis)
                yield data
