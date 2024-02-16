const hamburgerMenu = document.getElementById('menu-hamburger');
const openMenu = hamburgerMenu.querySelector('.open')
const closedMenu = hamburgerMenu.querySelector('.closed')
const menu = document.querySelector('.main-menu');

hamburgerMenu.addEventListener('click', function (event) {
    event.preventDefault();

    if (menu.style.display === "none" || menu.style.display === "") {
        menu.style.display = "block";
        openMenu.style.display = "block";
        closedMenu.style.display = "none";
    } else {
        menu.style.display = "none";
        openMenu.style.display = "none";
        closedMenu.style.display = "block";
    }
});

document.addEventListener('click', function (event) {
    if (!hamburgerMenu.contains(event.target) && !menu.contains(event.target)) {
        menu.style.display = "none";
        openMenu.style.display = "none";
        closedMenu.style.display = "block";
    }
});


// on pageshow event, if the menu is open, close it
window.addEventListener('pageshow', function (e) {
    if (e.persisted) {
        menu.style.display = "none";
        openMenu.style.display = "none";
        closedMenu.style.display = "block";
    }
});

export { }
