const hamburgerMenu = document.getElementById('menu-hamburger');
const openMenu = hamburgerMenu.querySelector('.open')
const closedMenu = hamburgerMenu.querySelector('.closed')
const menu = document.querySelector('.main-menu');

hamburgerMenu.addEventListener('click', function (event) {
    event.preventDefault();

    if (menu.style.display === "none") {
        menu.style.display = "block";
        openMenu.style.display = "block";
        closedMenu.style.display = "none";
    } else {
        menu.style.display = "none";
        openMenu.style.display = "none";
        closedMenu.style.display = "block";
    }
});

/**
 * Add resize event listener to window
 */
window.addEventListener('resize', function (event) {

    if (window.innerWidth > 768) {
        menu.style.display = "flex";
        openMenu.style.display = "none";
        closedMenu.style.display = "block";
    } else {
        menu.style.display = "none";
    }
});

export { }