const emotion_div = document.getElementById("emotion-div");
const val_arousal_div = document.getElementById("val-arousal-div");
const videoPlayer = document.getElementById('video-player');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let isPlaying = false;

function processFrame() {
    if (!isPlaying) {
        // exit if the video is paused
        return;
    }
    // get the current frame from the video
    ctx.drawImage(videoPlayer, 0, 0, canvas.width, canvas.height);
    const frame = canvas.toDataURL('image/jpeg', 0.8);
    fetch('/analyze_frame', {
        method: 'POST', body: JSON.stringify({frame: frame}), headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
        .then(data => {
            if (!data.face_img) return;
            face.src = 'data:image/jpeg;base64,' + data.face_img;
            emotions = data.emotions;
            if (emotions) {
                displayEmotions('emotion-div', emotions);
            }
            let val = data.valence;
            let arousal = data.arousal;
            if (val) {
                displayValenceArousal('val-arousal-div', val, arousal);
            }
        });
    // continue processing frames
    window.requestAnimationFrame(processFrame);
}

videoPlayer.addEventListener('play', function () {
    isPlaying = true;
    // start processing frames
    window.requestAnimationFrame(processFrame);
});

videoPlayer.addEventListener('pause', function () {
    isPlaying = false;
});

document.getElementById('video-file').addEventListener('change', function () {
    // set the source of the video player to the selected video file
    const videoFile = this.files[0];
    videoPlayer.src = URL.createObjectURL(videoFile);
});