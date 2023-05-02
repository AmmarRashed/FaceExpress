import base64
import os

import cv2
import numpy as np
from flask import Flask, render_template, jsonify, request

from src.facial_analysis import facial_analysis_pipeline
from src.feed import FrameGenerator
from src.gaze_tracking.gaze_tracking import GazeTracking

app = Flask(__name__)

frame_generator = FrameGenerator(video_src=None, analyze_face=True)
gaze_tracker = GazeTracking()
DATASET_ROOT = os.path.join("Engagement", "FaceEngageDataset")


@app.route('/webcam')
def webcam():
    return render_template("webcam.html")


@app.route('/video', methods=["POST", "GET"])
def video():
    if request.method == "POST":
        file = request.files["file"]
        file.save("gameplay")
        return render_template("video.html")
    return render_template("video.html")


@app.route("/analyze_frame", methods=["POST"])
def analyze_frame():
    frame = request.json['frame']
    img_bytes = base64.b64decode(frame.split(',')[1])
    # convert the decoded image to a numpy array using cv2
    image = np.frombuffer(img_bytes, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
    data = facial_analysis_pipeline(gaze_tracker, image)
    return jsonify(data)


@app.route("/frames")
def frames():
    global frame_generator
    video_src = request.args.get("video_src")
    if frame_generator.video_src != video_src:
        frame_generator = FrameGenerator(video_src=video_src, analyze_face=True)

    frame_data = frame_generator.gen_frames().__next__()
    return jsonify(frame_data)


@app.route("/_get_user_files", methods=["GET"])
def get_user_files():
    user = request.args.get("user")
    filenames = sorted({'.'.join(f.split(".")[:-1]) for f in os.listdir(os.path.join(DATASET_ROOT, user))
                        if f.startswith("u")})
    return filenames


@app.route("/samples", methods=["GET"])
def samples():
    return render_template("samples.html", users=sorted(os.listdir(DATASET_ROOT), key=lambda x: int(x[1:])))


if __name__ == '__main__':
    app.run()
