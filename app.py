from flask import Flask, render_template, Response

from scripts.feed import get_webcam_feed

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route("/video")
def video():
    return Response(get_webcam_feed(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':
    app.run()
