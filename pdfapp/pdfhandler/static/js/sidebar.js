document.addEventListener('DOMContentLoaded', function() {
    const usernameElement = document.querySelector('.sidebar .username');
    if (usernameElement && window.username) {
        usernameElement.textContent = window.username;
    }

    const userInfo = document.getElementById('userInfo');
    const sidebar = document.getElementById('sidebar');
    const closeSidebar = document.getElementById('closeSidebar');

    if (userInfo) {
        userInfo.addEventListener('click', function() {
            sidebar.classList.add('open');
        });
    }

    if (closeSidebar) {
        closeSidebar.addEventListener('click', function() {
            sidebar.classList.remove('open');
        });
    }

    const sections = document.querySelectorAll('.sidebar-section');
    
    sections.forEach(section => {
        section.addEventListener('click', function() {
            const sectionName = this.getAttribute('data-section');
            const submenu = document.getElementById(`submenu-${sectionName}`);
            
            if (submenu) {
                submenu.classList.toggle('open');
            }
        });
    });

    function handleLogout() {
        fetch('/logout/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/';
            }
        });
    }

    const logoutLink = document.getElementById('logoutLink');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            handleLogout();
        });
    }

    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', function(e) {
            e.preventDefault();
            handleLogout();
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});