/**
 * Burger menu
 */
document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('menu-hamburger').addEventListener('click', function(event) {
        event.preventDefault();
        const menu = document.querySelector('.main-menu');
        if (menu.style.display === "none" || menu.style.display === "") {
            menu.style.display = "block";
        } else {
            menu.style.display = "none";
        }
    });
});

export {}