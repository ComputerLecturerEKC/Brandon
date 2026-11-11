const toggle = document.getElementById("darkToggle");

toggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");

    const icon = document.body.classList.contains("dark-mode") ? "☀️" : "🌙";
    toggle.textContent = icon;

    localStorage.setItem("darkmode", document.body.classList.contains("dark-mode"));
});

// Load preference
if (localStorage.getItem("darkmode") === "true") {
    document.body.classList.add("dark-mode");
    toggle.textContent = "☀️";
}