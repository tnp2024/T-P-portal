document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector(".sidebar");
    const toggle = sidebar ? sidebar.querySelector(".toggle") : null;
    const searchBtn = sidebar ? sidebar.querySelector(".search-box") : null;
    const modeSwitch = sidebar ? sidebar.querySelector(".toggle-switch") : null;
    const modeText = sidebar ? sidebar.querySelector(".mode-text") : null;

    // Check if mode is stored in localStorage
    const isDarkMode = localStorage.getItem("darkMode") === "true";

    // Set initial mode based on localStorage or default to light mode
    if (isDarkMode) {
        document.body.classList.add("dark");
        if (modeText) {
            modeText.innerText = "Light mode";
        }
    } else {
        document.body.classList.remove("dark");
        if (modeText) {
            modeText.innerText = "Dark mode";
        }
    }



    // Toggle dark/light mode
    if (modeSwitch && modeText) {
        modeSwitch.addEventListener("click", () => {
            document.body.classList.toggle("dark");

            // Store mode in localStorage
            const isDarkMode = document.body.classList.contains("dark");
            localStorage.setItem("darkMode", isDarkMode);

            // Update mode text
            if (isDarkMode) {
                modeText.innerText = "Light mode";
            } else {
                modeText.innerText = "Dark mode";
            }
        });
    }
});