const emotion_div = document.getElementById("emotion-div");
const val_arousal_div = document.getElementById("val-arousal-div");
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
        width: 800,
        height: 800,
        yaxis: {
            tickfont: {
                size: 22
            }
        },
        xaxis:{range:[0, 1]}
    };
    Plotly.newPlot('emotion-div', data, layout);
}

// circle
var circle = {
    x: [],
    y: [],
    mode: 'lines',
    marker: {
        size: 2,
        color: 'black'
    }
};
var radius = 1;
for (var i = 0; i < 360; i++) {
    var angle = i * Math.PI / 180;
    var x = radius * Math.cos(angle);
    var y = radius * Math.sin(angle);
    circle.x.push(x);
    circle.y.push(y);
}

function displayValenceArousal(val, arousal) {
    val_arousal_div.innerHTML = "";
    var layout = {
        xaxis: {
            range: [-1.2, 1.2],
            zeroline: true,
            zerolinewidth: 2,
            showgrid: true,
            gridcolor: 'grey',
            zerolinecolor: 'black'
        },
        yaxis: {
            range: [-1.2, 1.2],
            zeroline: true,
            zerolinewidth: 2,
            showgrid: true,
            gridcolor: 'grey',
            zerolinecolor: 'black'
        },
        plot_bgcolor: "white",
        width: 800,
        height: 800,
        title: 'Valence-Arousal Plot',
        showlegend: false,
        annotations: [
            {x: -1, y: 0, text: "Negative", font: {"color": "red", "size": 16}, showarrow: false, bgcolor: "white"},
            {x: 1, y: 0, text: "Positive", font: {"color": "green", "size": 16}, showarrow: false, bgcolor: "white"},
            {x: 0, y: 0, text: "Neutral", font: {"size": 16}, showarrow: false, bgcolor: "white"},
            {x: 0.9, y: 0.2, text: "Happy", font: {"size": 16}, showarrow: false, bgcolor: "white"},
            {x: 0.4, y: 0.9, text: "Surprise", font: {"size": 16}, showarrow: false, bgcolor: "white"},
            {x: -0.2, y: 0.9, text: "Fear", font: {"size": 16}, showarrow: false, bgcolor: "white"},
            {x: -0.9, y: 0.4, text: "Disgust", font: {"size": 16}, showarrow: false, bgcolor: "white"},
            {x: -0.8, y: 0.6, text: "Contempt", font: {"size": 16}, showarrow: false, bgcolor: "white"},
            {x: -0.6, y: 0.8, text: "Anger", font: {"size": 16}, showarrow: false, bgcolor: "white"},
            {x: -0.9, y: -0.4, text: "Sad", font: {"size": 16}, showarrow: false, bgcolor: "white"},
            {x: 0, y: 1.1, text: "Excited", font: {"color": "orange", "size": 16}, showarrow: false, bgcolor: "white"},
            {x: 0, y: -1.1, text: "Calm", font: {"color": "blue", "size": 16}, showarrow: false, bgcolor: "white"}
        ]
    }

    var data = [
        circle,
        {mode: 'markers', x:[val], y:[arousal], name:'Emotion', marker:{color:'red', size:16}}
    ]
    Plotly.newPlot('val-arousal-div', data, layout);
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
            face.src = 'data:image/jpeg;base64,' + response.face_img;
            emotions = response.emotions;
            if (emotions) {
                displayEmotions(emotions);
            }
            let val = response.valence;
            let arousal = response.arousal;
            if (val) {
                displayValenceArousal(val, arousal);
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