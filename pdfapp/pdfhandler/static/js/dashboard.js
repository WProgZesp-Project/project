document.getElementById("userInfo").addEventListener("click", function () {
    document.getElementById("sidebar").classList.add("open");
});

document.getElementById("closeSidebar").addEventListener("click", function () {
    document.getElementById("sidebar").classList.remove("open");
});

function toggleSubmenu(section) {
    const submenu = document.getElementById(`submenu-${section}`);
    if (submenu) {
        submenu.classList.toggle('open');
    }
}

function logout() {
    const token = localStorage.getItem("authToken");
    if (!token) {
        window.location.href = "/";
        return;
    }

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
}
  