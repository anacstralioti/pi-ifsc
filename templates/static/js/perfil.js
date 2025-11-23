document.addEventListener("DOMContentLoaded", function() {
    const btn = document.getElementById("perfilMenuBtn");
    const menu = document.getElementById("perfilDropdown");

    if (btn) {
        btn.addEventListener("click", () => {
            menu.classList.toggle("hidden");
        });

        document.addEventListener("click", (e) => {
            if (!btn.contains(e.target) && !menu.contains(e.target)) {
                menu.classList.add("hidden");
            }
        });
    }

    const fileInput = document.getElementById('foto');
    const fileNameSpan = document.getElementById('file-name');

    if (fileInput && fileNameSpan) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                fileNameSpan.textContent = this.files[0].name;
            } else {
                fileNameSpan.textContent = 'Selecione um arquivo';
            }
        });
    }
});