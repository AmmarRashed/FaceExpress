from flask import Flask, render_template, jsonify, request

from src.feed import FrameGenerator

app = Flask(__name__)

frame_generator = FrameGenerator(video_src=None, analyze_face=True)


@app.route('/webcam')
def webcam():
    return render_template("webcam.html")


@app.route('/video')
def video():
    return render_template("video.html")


# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # handle file upload
#         file = request.files['file']
#         print(file)
#         # do something with the file here
#         return 'file uploaded successfully'
#     # display the form
#     return render_template('webcam.html')

@app.route("/analyze_frame", methods=["POST"])
def analyze_frame():
    frame = request.json['frame']
    print("Received frame")
    return "Success"


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
