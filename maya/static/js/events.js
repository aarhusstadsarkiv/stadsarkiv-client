class Events {

    /**
     * Add event listener to multiple elements
     * @param {*} selector 
     * @param {*} eventName 
     * @param {*} callback 
     */
    static addEventListenerMultiple(selector, eventName, callback) {
        const elements = document.querySelectorAll(selector);

        elements.forEach(function (element) {
            element.addEventListener(eventName, callback);
        });
    }
}

export { Events }
