document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("perfilMenuBtn");
    const menu = document.getElementById("perfilDropdown");

    if (btn) {
      btn.addEventListener("click", () => {
        menu.classList.toggle("hidden");
      });

-      document.addEventListener("click", (e) => {
        if (!btn.contains(e.target) && !menu.contains(e.target)) {
          menu.classList.add("hidden");
        }
      });
    }
  });