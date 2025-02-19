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

    // Play/Pause
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

    // Форматирование времени в формате MM:SS
    function formatTime(time) {
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60);
        return `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    }

    // Обновляет длительность трека
    audioPlayer.addEventListener("loadedmetadata", () => {
        durationElement.textContent = formatTime(audioPlayer.duration);
    });

    // Обновляет текущее время и прогресс-бар
    audioPlayer.addEventListener("timeupdate", () => {
        const currentTime = audioPlayer.currentTime;
        currentTimeElement.textContent = formatTime(currentTime);
        const percent = (currentTime / audioPlayer.duration) * 100;
        progress.style.width = `${percent}%`;
    });

    // Перематывание трека по клику на прогресс-бар
    function setProgress(event) {
        const barWidth = progressBar.clientWidth;
        const clickX = event.clientX - progressBar.getBoundingClientRect().left;
        const duration = audioPlayer.duration;

        if (!isNaN(duration) && duration > 0) {
            audioPlayer.currentTime = Math.min((clickX / barWidth) * duration, duration - 0.1);
            console.log("Перемотано на:", audioPlayer.currentTime);
        }
    }

    if (progressBar) {
        progressBar.addEventListener("click", setProgress);
    } else {
        console.error("Прогресс-бар не найден!");
    }

    // Управление громкостью
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

    // Переключение треков
    document.querySelectorAll(".track").forEach(track => {
        track.addEventListener("click", function () {
            const trackSrc = this.getAttribute("data-src");
            const logoSrc = this.getAttribute("data-logo");
            const trackName = this.getAttribute("data-name");
            const trackAuthorName = this.getAttribute("data-author");

            if (trackSrc) {
                audioPlayer.src = trackSrc;
                audioPlayer.play();

                trackLogo.src = logoSrc;
                trackTitle.textContent = trackName;
                trackAuthor.textContent = trackAuthorName;

                playIcon.classList.remove("fa-play");
                playIcon.classList.add("fa-pause");
            }
        });
    });
});
