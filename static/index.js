var webcam_feed = document.getElementById("webcam-feed");
var emotion_div = document.getElementById("emotion-div");
var pause_btn = document.getElementById("pause-btn");
var pause_state = false;

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
    if (pause_state)
        return;
    $.ajax({
        type: 'GET',
        url: '/webcam',
        success: function (response) {
            emotions = response.emotions;
            if (emotions) {
                displayEmotions(emotions);
            }
            webcam_feed.src = 'data:image/jpeg;base64,' + response.frame;
        },
    })
}

function togglePause() {
    pause_state = !pause_state;
    if (pause_state)
        pause_btn.innerHTML = "Resume";
    else
        pause_btn.innerHTML = "Pause";
}

setInterval(get_frame, 50)