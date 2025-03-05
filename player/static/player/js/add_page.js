document.getElementById('id_logo').addEventListener('change', function (e) {
    const [file] = e.target.files;
    if (file) {
        const preview = document.getElementById('cover-preview');
        preview.src = URL.createObjectURL(file);
        preview.style.display = 'block';
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.querySelector('.track-search-input');
    const trackItems = document.querySelectorAll('.track-select-container div');

    searchInput.addEventListener('input', function (e) {
        const searchTerm = e.target.value.toLowerCase();

        trackItems.forEach(item => {
            const trackName = item.querySelector('label').textContent.toLowerCase();
            item.style.display = trackName.includes(searchTerm) ? 'flex' : 'none';
        });
    });
});