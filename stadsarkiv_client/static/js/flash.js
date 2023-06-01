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
}, 20000);

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

    static setFlashMessage(str, type, remove_after) {
        var messageElem = document.querySelector(".flash-messages");
        messageElem.innerHTML = '';

        if (!type) {
            type = 'notice';
        }

        let class_random = '';
        if (remove_after) {
            class_random = 'random_' + (Math.random() + 1).toString(36).substring(2);
            setTimeout(function () {
                let elem = document.querySelector('.' + class_random)
                if (elem) {
                    elem.remove();
                }
            }, remove_after)
        }

        var html = `<div class="flash flash-${type} ${class_random}">${str}</div>`;
        messageElem.insertAdjacentHTML('afterbegin', html);
        messageElem.scrollIntoView();
    }
}

// On screen resize, set the width of the flash messages
window.addEventListener('resize', function () {
    Flash.setWidth()
})

export {Flash}

// document.getElementById("mydiv").offsetWidth