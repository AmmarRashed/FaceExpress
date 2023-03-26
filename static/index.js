var webcam_feed = document.getElementById("webcam-feed");

function get_frame() {
    $.ajax({
        type: 'GET',
        url: '/webcam',
        success: function (data) {
            emotions = response.emotions;
            if (emotions)
                emotions = JSON.parse(response.emotions);
            console.log("Emotions: "+emotions);
            webcam_feed.src = 'data:image/jpeg;base64,' + data.frame;
        },
    })
}

setInterval(get_frame, 20)