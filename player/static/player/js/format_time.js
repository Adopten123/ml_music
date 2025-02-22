document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".track").forEach(track => {
        let durationElement = track.querySelector(".track-duration");
        let rawDuration = track.getAttribute("data-duration"); // Получаем исходное значение

        if (rawDuration) {
            let formattedDuration = rawDuration.replace(/\./g, ":"); // Заменяем все точки на двоеточия
            durationElement.textContent = formattedDuration;
        }
    });
});