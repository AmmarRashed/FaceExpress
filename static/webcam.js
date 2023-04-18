const emotion_div = document.getElementById("emotion-div");
const val_arousal_div = document.getElementById("val-arousal-div");
const webcam_feed = document.getElementById("webcam-feed");
const face = document.getElementById("face");
const pause_btn = document.getElementById("pause-btn");
let pause_state = false;
let stream_interval;


function get_frame() {
    if (pause_state) {
        console.log("Paused")
        return;
    }
    $.ajax({
        type: 'GET',
        data: {'video_src': 0},
        url: '/frames',
        success: function (response) {
            face.src = 'data:image/jpeg;base64,' + response.face_img;
            emotions = response.emotions;
            if (emotions) {
                displayEmotions("emotion-div", emotions);
            }
            let val = response.valence;
            let arousal = response.arousal;
            if (val) {
                displayValenceArousal('val-arousal-div', val, arousal);
            }
            webcam_feed.src = 'data:image/jpeg;base64,' + response.frame;
        },
    })

    stream_interval = setTimeout(get_frame, 100);
}

function togglePause() {
    pause_state = !pause_state;
    if (pause_state) {
        pause_btn.innerHTML = "Resume";
        clearTimeout(stream_interval);
    } else {
        pause_btn.innerHTML = "Pause";
        stream_interval = setTimeout(get_frame, 100);
    }
}

get_frame();