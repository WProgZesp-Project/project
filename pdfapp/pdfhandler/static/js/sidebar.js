document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".username").forEach(el => {
        el.textContent = window.username;
    });
    
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
                "Content-Type": "application/json"
            }
        }).then(() => {
            document.cookie = "auth_token=; Max-Age=0; path=/";
            window.location.href = "/";
        });
    });
});
