const usersDropdown = document.getElementById("users_dropdown");
const filesDropdown = document.getElementById("files_dropdown");
const videoPlayer = document.getElementById('video-player');

function populateFilesDropdown() {
    filesDropdown.innerHTML = '';
    fetch("/_get_user_files?user=" + usersDropdown.value)
        .then(response => response.json())
        .then(files => {
            files.forEach(function (filename) {
                var option = document.createElement('option');
                option.value = filename;
                option.text = filename;
                filesDropdown.appendChild(option);
            })
        });
}

usersDropdown.addEventListener('change', populateFilesDropdown);


videoPlayer.addEventListener('play', function () {
    isPlaying = true;
    // start processing frames
    window.requestAnimationFrame(processFrame);
});

videoPlayer.addEventListener('pause', function () {
    isPlaying = false;
});

function loadData() {

    fetch("/_load_user_video?user=" + usersDropdown.value + "?clip=" + filesDropdown.value)
        .then(response => response.json())
        .then(data => {
            console.log("TODO");
        });
}

filesDropdown.addEventListener('change', loadData);

populateFilesDropdown();
loadData();