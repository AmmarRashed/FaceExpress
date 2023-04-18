function displayEmotions(div, emotions) {
    emotion_div.innerHTML = "";
    var x = [];
    var y = [];
    for (const [em, val] of Object.entries(emotions)) {
        x.push(val);
        y.push(em);
    }
    var data = [{
        type: 'bar', x: x, y: y, orientation: 'h'
    }];
    var layout = {
        width: 800, height: 800,
        yaxis: {
            tickfont: {
                size: 22
            }
        }
        ,
        xaxis: {range: [0, 1]}
    };
    Plotly.newPlot(div, data, layout);
}

// circle
var circle = {
    x: [], y: [], mode: 'lines', marker: {
        size: 2, color: 'black'
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

function displayValenceArousal(div, val, arousal) {
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
        annotations: [{
            x: -1,
            y: 0,
            text: "Negative",
            font: {"color": "red", "size": 16},
            showarrow: false,
            bgcolor: "white"
        }, {
            x: 1,
            y: 0,
            text: "Positive",
            font: {"color": "green", "size": 16},
            showarrow: false,
            bgcolor: "white"
        }, {x: 0, y: 0, text: "Neutral", font: {"size": 16}, showarrow: false, bgcolor: "white"}, {
            x: 0.9,
            y: 0.2,
            text: "Happy",
            font: {"size": 16},
            showarrow: false,
            bgcolor: "white"
        }, {x: 0.4, y: 0.9, text: "Surprise", font: {"size": 16}, showarrow: false, bgcolor: "white"}, {
            x: -0.2,
            y: 0.9,
            text: "Fear",
            font: {"size": 16},
            showarrow: false,
            bgcolor: "white"
        },
            {x: -0.9, y: 0.4, text: "Disgust", font: {"size": 16}, showarrow: false, bgcolor: "white"},
            {x: -0.8, y: 0.6, text: "Contempt", font: {"size": 16}, showarrow: false, bgcolor: "white"},
            {x: -0.6, y: 0.8, text: "Anger", font: {"size": 16}, showarrow: false, bgcolor: "white"},
            {x: -0.9, y: -0.4, text: "Sad", font: {"size": 16}, showarrow: false, bgcolor: "white"}, {
                x: 0,
                y: 1.1,
                text: "Excited",
                font: {"color": "orange", "size": 16},
                showarrow: false,
                bgcolor: "white"
            }, {x: 0, y: -1.1, text: "Calm", font: {"color": "blue", "size": 16}, showarrow: false, bgcolor: "white"}]
    }

    var data = [circle, {mode: 'markers', x: [val], y: [arousal], name: 'Emotion', marker: {color: 'red', size: 16}}]
    Plotly.newPlot(div, data, layout);
}
