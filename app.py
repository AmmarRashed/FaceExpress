from flask import Flask, render_template, Response, jsonify

from utils.feed import FrameGenerator

app = Flask(__name__)

frame_generator = FrameGenerator(analyze_face=True)


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route("/webcam")
def webcam():
    frame_data = frame_generator.gen_frames().__next__()
    return jsonify(frame_data)


if __name__ == '__main__':
    app.run()
