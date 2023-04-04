const emotion_div = document.getElementById("emotion-div");
const videoPlayer = document.getElementById('video-player');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let isPlaying = false;
let frameCount = 0;

function displayEmotions(emotions) {
    emotion_div.innerHTML = "";
    var x = [];
    var y = [];
    for (const [em, val] of Object.entries(emotions)) {
        x.push(val);
        y.push(em);
    }
    var data = [{
        type: 'bar',
        x: x,
        y: y,
        orientation: 'h'
    }];
    var layout = {
        width: 600,
        yaxis: {
            tickfont: {
                size: 22
            }
        }
    };
    Plotly.newPlot('emotion-div', data, layout);
}

function processFrame() {
    if (!isPlaying) {
        // exit if the video is paused
        return;
    }
    // get the current frame from the video
    ctx.drawImage(videoPlayer, 0, 0, canvas.width, canvas.height);
    const frame = canvas.toDataURL('image/jpeg', 0.8);
    fetch('/analyze_frame', {
        method: 'POST',
        body: JSON.stringify({frame: frame}),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(response => response.json())
        .then(data => {
            let emotions = data.emotions;
            if (emotions) {
                displayEmotions(emotions);
                face.src = 'data:image/jpeg;base64,' + data.face;
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