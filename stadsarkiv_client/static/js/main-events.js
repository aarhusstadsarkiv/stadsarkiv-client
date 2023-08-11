document.getElementById('menu-hamburger').addEventListener('click', function (event) {
    event.preventDefault();
    const menu = document.querySelector('.main-menu');
    const menuText = document.querySelector('#menu-hamburger > .material-symbols-outlined');
    if (menu.style.display === "none" || menu.style.display === "") {
        menu.style.display = "block";
        menuText.textContent = "menu_open";
    } else {
        menu.style.display = "none";
        menuText.textContent = "menu";
    }
});

/**
 * Add resize event listener to window
 */
window.addEventListener('resize', function (event) {
    const menuText = document.querySelector('#menu-hamburger > .material-symbols-outlined');
    const menu = document.querySelector('.main-menu');
    if (window.innerWidth > 768) {
        menu.style.display = "flex";
        menuText.textContent = "menu";
    } else {
        menu.style.display = "none";
    }
});

export { }