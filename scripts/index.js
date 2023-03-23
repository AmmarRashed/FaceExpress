console.log("HELLo!");
function update() {
    console.log("Updating!")
    // Make an AJAX request to get the current frame and string
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/video');

    xhr.onload = function () {
        if (xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);

            // Update the image source and display the string
            document.getElementById('frame').src = data.frame;
            document.getElementById('emotion').innerHTML = data.emotion;
        }
    };

    xhr.send();
}

// Update the page every second
setInterval(update, 33);