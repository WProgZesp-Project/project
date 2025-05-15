document.addEventListener("DOMContentLoaded", function () {
    const token = localStorage.getItem("authToken");
    if (!token) {
        window.location.href = "/";
        return;
    }

    // Get username
    const username = localStorage.getItem("authUsername");
    if (username) {
        const usernameSpan = document.querySelector(".username");
        if (usernameSpan) {
            usernameSpan.textContent = username;
        }
    }

    // Sidebar toggle
    document.getElementById("userInfo")?.addEventListener("click", function () {
        document.getElementById("sidebar")?.classList.add("open");
    });

    document.getElementById("closeSidebar")?.addEventListener("click", function () {
        document.getElementById("sidebar")?.classList.remove("open");
    });

    // Submenu toggle
    document.querySelectorAll(".sidebar-section").forEach(section => {
        section.addEventListener("click", function () {
            const name = section.dataset.section;
            const submenu = document.getElementById(`submenu-${name}`);
            if (submenu) submenu.classList.toggle("open");
        });
    });

    // Logout
    document.getElementById("logoutLink")?.addEventListener("click", function (e) {
        e.preventDefault();
        fetch("/logout/", {
            method: "POST",
            headers: {
                "Authorization": "Token " + token,
                "Content-Type": "application/json"
            }
        }).then(() => {
            localStorage.removeItem("authToken");
            window.location.href = "/";
        });
    });
});
