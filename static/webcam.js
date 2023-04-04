const emotion_div = document.getElementById("emotion-div");
const webcam_feed = document.getElementById("webcam-feed");
const face = document.getElementById("face");
const pause_btn = document.getElementById("pause-btn");
let pause_state = false;
let stream_interval;

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
            emotions = response.emotions;
            if (emotions) {
                displayEmotions(emotions);
                face.src = 'data:image/jpeg;base64,' + response.face;
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