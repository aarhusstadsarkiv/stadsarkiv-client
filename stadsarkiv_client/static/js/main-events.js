/**
 * Burger menu
 */


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

const menu = document.querySelector('.main-menu');
menu.style.display = "none";

export { }