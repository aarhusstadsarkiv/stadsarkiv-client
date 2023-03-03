/**
 * Remove pre-loaded flash messages after some seconds
 */
function removeFlashMessages() {
    let elems = document.querySelectorAll('.flash-remove')
    elems.forEach(function (elem) {
        elem.remove();
    })
}

setTimeout(function () {
    removeFlashMessages();
}, 5000);

/**
 * Remove flash messages when clicked
 */
document.addEventListener("click", function (e) {
    if (e.target.classList.contains('flash')) {
        e.target.remove();
    }
})

class Flash {
    static setWidth() {
        let containerElem = document.querySelector('.container')
        let flashMessagesElem = document.querySelector('.flash-messages')
        flashMessagesElem.style.width = containerElem.offsetWidth + "px"
    }
}

// On screen resize, set the width of the flash messages
window.addEventListener('resize', function () {
    Flash.setWidth()
})

export {Flash}

// document.getElementById("mydiv").offsetWidth