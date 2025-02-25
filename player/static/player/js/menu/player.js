document.addEventListener("DOMContentLoaded", () => {
    const audioPlayer = document.getElementById("audio-player");
    const playPauseBtn = document.getElementById("play-pause-btn");
    const playIcon = document.getElementById("play-icon");
    const currentTimeElement = document.getElementById("current-time");
    const progressBar = document.querySelector(".progress-bar");
    const progress = document.getElementById("progress");
    const durationElement = document.getElementById("duration");
    const volumeSlider = document.getElementById("volume-slider");
    const volumeDownBtn = document.getElementById("volume-down-btn");
    const volumeUpBtn = document.getElementById("volume-up-btn");
    const trackLogo = document.getElementById("track-logo");
    const trackTitle = document.getElementById("track-title");
    const trackAuthor = document.getElementById("track-author");
    const tracks = document.querySelectorAll(".track");
    let currentTrackIndex = 0;

    function togglePlayPause() {
        if (audioPlayer.paused) {
            audioPlayer.play();
            playIcon.classList.remove("fa-play");
            playIcon.classList.add("fa-pause");
        } else {
            audioPlayer.pause();
            playIcon.classList.remove("fa-pause");
            playIcon.classList.add("fa-play");
        }
    }

    playPauseBtn.addEventListener("click", togglePlayPause);

    function formatTime(time) {
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60);
        return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    }

    audioPlayer.addEventListener("loadedmetadata", () => {
        durationElement.textContent = formatTime(audioPlayer.duration);
    });

    audioPlayer.addEventListener("timeupdate", () => {
        const currentTime = audioPlayer.currentTime;
        currentTimeElement.textContent = formatTime(currentTime);
        const percent = (currentTime / audioPlayer.duration) * 100;
        progress.style.width = `${percent}%`;
    });

    function setProgress(event) {
        const barWidth = progressBar.clientWidth;
        const clickX = event.clientX - progressBar.getBoundingClientRect().left;
        const duration = audioPlayer.duration;

        if (!isNaN(duration) && duration > 0) {
            audioPlayer.currentTime = Math.min((clickX / barWidth) * duration, duration - 0.1);
        }
    }

    if (progressBar) {
        progressBar.addEventListener("click", setProgress);
    }

    volumeSlider.addEventListener("input", (e) => {
        audioPlayer.volume = e.target.value;
    });

    volumeDownBtn.addEventListener("click", () => {
        audioPlayer.volume = Math.max(audioPlayer.volume - 0.1, 0);
        volumeSlider.value = audioPlayer.volume;
    });

    volumeUpBtn.addEventListener("click", () => {
        audioPlayer.volume = Math.min(audioPlayer.volume + 0.1, 1);
        volumeSlider.value = audioPlayer.volume;
    });

    function loadTrack(index) {
        if (index >= 0 && index < tracks.length) {
            const track = tracks[index];
            audioPlayer.src = track.getAttribute("data-src");
            trackLogo.src = track.getAttribute("data-logo");
            trackTitle.textContent = track.getAttribute("data-name");
            trackAuthor.textContent = track.getAttribute("data-author");
            currentTrackIndex = index;
            audioPlayer.play();
            playIcon.classList.remove("fa-play");
            playIcon.classList.add("fa-pause");
        }
    }

    tracks.forEach((track, index) => {
        track.addEventListener("click", () => loadTrack(index));
    });

    audioPlayer.addEventListener("ended", () => {
        let nextTrackIndex = (currentTrackIndex + 1) % tracks.length;
        loadTrack(nextTrackIndex);
    });
});
