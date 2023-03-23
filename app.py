from flask import Flask, render_template, Response, jsonify

from utils.feed import get_webcam_feed

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route("/video")
def video():
    frame, emotion = get_webcam_feed()
    # response = Response(frame, mimetype="multipart/x-mixed-replace; boundary=frame")
    return jsonify({"frame": frame, "emotion": emotion})


if __name__ == '__main__':
    app.run()
