/**
 * Remove pre-loaded flash messages after some seconds
 */
function removeFlashMessages() {
    let elems = document.querySelectorAll('.flash-remove')
    elems.forEach(function (elem) {
        elem.remove();
    })
}

const removeAfterSecs = 20;

/**
 * Remove loaded flash messages after some seconds
 */
setTimeout(function () {
    removeFlashMessages();
}, removeAfterSecs * 1000);

/**
 * Remove flash messages when clicked
 */
document.addEventListener("click", function (e) {
    if (e.target.classList.contains('flash')) {
        e.target.remove();
    }
})

class Flash {

    /**
     * Set a flash message
     * @param {str} The message to display
     * @param {type}  'info', 'success', 'warning', 'error' or any other you may use in your app. 
     * @param {remove_after} remove the message after some seconds 
     */
    static setMessage(message, type, remove_after) {
        const messageElem = document.querySelector(".flash-messages");
        messageElem.focus();
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
            }, removeAfterSecs * 1000)
        }

        const html = `<div class="flash flash-${type} ${class_random}">${message}</div>`;
        messageElem.insertAdjacentHTML('afterbegin', html);
    }
}

export {Flash}
