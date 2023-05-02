from imutils.video import WebcamVideoStream, FileVideoStream

from src.facial_analysis import analyze_face, detect_face, track_eyes
from src.gaze_tracking.gaze_tracking import GazeTracking
from src.utils import encode_frame


class FrameGenerator(object):
    def __init__(self, video_src, analyze_face=True):
        self.video_src = video_src
        self.video = WebcamVideoStream(0) if video_src == "0" else FileVideoStream(self.video_src)
        self.video.start()
        self.analyze_face = analyze_face
        self.gaze_tracker = GazeTracking()

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
                if self.analyze_face:
                    analysis = analyze_face(face[:, :, ::-1], keep_face=False, keep_landmarks=True)  # correct colors
                    eye_data, face = track_eyes(self.gaze_tracker, face, analysis.pop("landmarks"))
                    data.update(analysis)
                    data.update(eye_data)
                data["face_img"] = encode_frame(face)
                yield data
