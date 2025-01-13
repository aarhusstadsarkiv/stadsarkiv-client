const hamburgerMenu = document.getElementById('menu-hamburger');
const openMenu = hamburgerMenu.querySelector('.open');
const closedMenu = hamburgerMenu.querySelector('.closed');
const menu = document.querySelector('.main-menu-overlay');

hamburgerMenu.addEventListener('click', function (event) {
    event.preventDefault();

    // Expand
    if (menu.style.display === "none" || menu.style.display === "") {
        menu.style.display = "block";
        openMenu.style.display = "block";
        closedMenu.style.display = "none";
        hamburgerMenu.setAttribute('aria-expanded', 'true');
    } else {
        menu.style.display = "none";
        openMenu.style.display = "none";
        closedMenu.style.display = "block";
        hamburgerMenu.setAttribute('aria-expanded', 'false');
    }
});

document.addEventListener('click', function (event) {
    if (!hamburgerMenu.contains(event.target) && !menu.contains(event.target)) {
        menu.style.display = "none";
        openMenu.style.display = "none";
        closedMenu.style.display = "block";
        hamburgerMenu.setAttribute('aria-expanded', 'false');
    }
});


// on pageshow event, if the menu is open, close it
window.addEventListener('pageshow', function (e) {
    if (e.persisted) {
        menu.style.display = "none";
        openMenu.style.display = "none";
        closedMenu.style.display = "block";
        hamburgerMenu.setAttribute('aria-expanded', 'false');
    }
});

const actionLinks = document.querySelectorAll('.action-links > a');
let activeLinkSet = false;

actionLinks.forEach(link => {
    const path = link.getAttribute('data-path') || link.getAttribute('href');
    const isExactMatch = path === window.location.pathname;
    const isPartialMatch = path !== '/' && window.location.pathname.startsWith(path);

    if (isExactMatch || isPartialMatch) {
        link.classList.add('active');
        activeLinkSet = true;
    }
});
