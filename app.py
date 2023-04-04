import base64

import cv2
import numpy as np
from flask import Flask, render_template, jsonify, request

from src.facial_analysis import facial_analysis_pipeline
from src.feed import FrameGenerator
from src.utils import encode_frame

app = Flask(__name__)

frame_generator = FrameGenerator(video_src=None, analyze_face=True)


@app.route('/webcam')
def webcam():
    return render_template("webcam.html")


@app.route('/upload_video')
def upload_video():
    return render_template("upload_video.html")


@app.route("/analyze_frame", methods=["POST"])
def analyze_frame():
    frame = request.json['frame']
    img_bytes = base64.b64decode(frame.split(',')[1])
    # convert the decoded image to a numpy array using cv2
    image = np.frombuffer(img_bytes, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED)
    data = facial_analysis_pipeline(image)
    return jsonify(data)


@app.route("/frames")
def frames():
    global frame_generator
    video_src = request.args.get("video_src")
    if video_src == "0":
        video_src = 0
    if frame_generator.video_src != video_src:
        frame_generator = FrameGenerator(video_src=video_src, analyze_face=True)

    frame_data = frame_generator.gen_frames().__next__()
    return jsonify(frame_data)


if __name__ == '__main__':
    app.run()
