from flask import Flask, render_template, jsonify

from src.feed import FrameGenerator

app = Flask(__name__)

frame_generator = None


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route("/webcam")
def webcam():
    global frame_generator
    if frame_generator is None:
        frame_generator = FrameGenerator(analyze_face=True)
    frame_data = frame_generator.gen_frames().__next__()
    return jsonify(frame_data)


if __name__ == '__main__':
    app.run()
