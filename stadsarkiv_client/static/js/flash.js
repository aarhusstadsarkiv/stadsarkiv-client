/* 

Very basic flash messages for server-side and javascript.

// Flash messages looks like this:
<div class="flash-messages">
	<div class="flash flash-error">Email eller password er ikke korrekt.</div>
</div>

// Remove flash messages on page load
<script type="module">
    import { Flash } from "/static/js/flash.js";
    Flash.clearMessages(5); 
	// Comment out if you want to keep the messages until user clicks on them

	// Set a flash message
	Flash.setMessage('This is a flash message', 'success', 5);

	// Will add a div to "flash-messages" 
	// With the classes "flash flash-success random_..." and remove it after 5 seconds

	// Flash.setMessage('This is a flash message', 'success');
	// Will add a div to "flash-messages" with the classes "flash flash-success" and keep it until removed
	// or user clicks on it
</script>

*/

class Flash {


    /**
     * Set a flash message
     * @param {str} The message to display
     * @param {type}  'info', 'success', 'warning', 'error' or any other you may use in your app. 
     * @param {removeAfterSecs} remove
     */
    static setMessage(message, type, removeAfterSecs = null) {
        const messageElem = document.querySelector(".flash-messages");
        messageElem.focus();
        messageElem.innerHTML = '';

        if (!type) {
            type = 'notice';
        }

        let class_random = '';
        if (removeAfterSecs) {
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

    /**
     * Remove all flash messages after page load
     */
    static clearMessages(removeAfterSecs) {

        setTimeout(function () {
            let elems = document.querySelectorAll('.flash-remove')
            elems.forEach(function (elem) {
                elem.remove();
            })
        }, removeAfterSecs * 1000)
    }
}

document.addEventListener("click", function (e) {
    if (e.target.classList.contains('flash')) {
        e.target.remove();
    }
})

export { Flash }
