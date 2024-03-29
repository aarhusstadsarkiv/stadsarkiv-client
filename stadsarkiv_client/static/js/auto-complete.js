/**
 * Default return function. 
 * Checks if the focused item has a data-url attribute and redirects to that URL.
 */
function returnFunction(focusedItem) {
    const url = focusedItem.getAttribute('data-url');
    if (url) {
        window.location.href = url;
        return;
    }
}

class AutoComplete {
    constructor(options) {

        // Required parameters
        this.autocompleteElem = options.autocompleteElem; 
        this.suggestionsElem = options.suggestionsElem;
        this.renderFunction = options.renderFunction;
        this.endpoint = options.endpoint;

        // Optional parameters
        this.debounceTimer = options.debounceTimer || 500;
        this.lastInputValue = options.lastInputValue || ''; // Last input value. Used to prevent fetching the same value multiple times
        this.minInputLength = options.minInputLength || 2; 
        this.suggestionFocusClass = options.suggestionFocusClass || 'search-suggestion-focused'; // Class for focused suggestion item
        this.suggestionItemClass = options.suggestionItemClass || 'search-suggestion-item'; // Class for normal suggestion items
        this.returnFunction = options.returnFunction || returnFunction; // Function to run when a suggestion is selected
        this.debug = options.debug || false;
        
        this.preventOverflow = options.preventOverflow || false; // Prevent suggestions from overflowing the window
        this.overflowSpace = options.overflowSpace || 20; // Minimum space between suggestions and the bottom of the window in pixels

        // Debounce timeout ID
        this.timeoutID = null;

        // Bind methods
        this.autocompleteElem.addEventListener('input', this.onInput.bind(this));
        this.autocompleteElem.addEventListener('keydown', this.onKeyDown.bind(this));

        // Bind the onBlur method
        this.onBlur = this.onBlur.bind(this);

        // Add the blur event listener
        this.autocompleteElem.addEventListener('blur', this.onBlur);

        // Hide suggestions on resize
        window.addEventListener('resize', this.hideSuggestions.bind(this));

        // Hide suggestions on load
        this.hideSuggestions();
    }

    onBlur() {
        // Set a short timeout to allow clicks on suggestions to register
        setTimeout(() => {
            if (!this.debug) {
                this.hideSuggestions();
            }
        }, this.debounceTimer);
    }

    hideSuggestions() {
        // Hide suggestions on resize and empty the suggestions
        this.suggestionsElem.style.display = 'none';
        this.suggestionsElem.innerHTML = '';
    }

    onInput(e) {

        clearTimeout(this.timeoutID);
        const inputLength = this.autocompleteElem.value.length;
        const inputValue = e.target.value;

        if (inputLength < this.minInputLength) {
            this.hideSuggestions();
            return;
        }

        // Do not fetch if the input value if it is the same as the last input value
        if (inputValue === this.lastInputValue) return;
        this.lastInputValue = inputValue;

        this.timeoutID = setTimeout(() => {
            fetch(`${this.endpoint}${inputValue}`)
                .then(response => response.json())
                .then(data => {
                    this.updateSuggestions(data)
                });
        }, this.debounceTimer);
    }

    /**
     * Check keys pressed in the input field
     */
    onKeyDown(e) {

        const items = this.suggestionsElem.querySelectorAll(`.${this.suggestionItemClass}`);
        if (items.length === 0 && e.key !== 'Escape') return;

        if (e.key === 'Escape') {
            e.preventDefault();
            this.hideSuggestions();
            return;
        }

        let currentIndex = -1;
        items.forEach((item, index) => {
            if (item.classList.contains(this.suggestionFocusClass)) {
                currentIndex = index;
                item.classList.remove(this.suggestionFocusClass);
            }
        });

        if (e.key === 'ArrowDown') {
            currentIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
        } else if (e.key === 'ArrowUp') {
            currentIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
        } else if (e.key === 'Enter' && currentIndex !== -1) {
            e.stopPropagation(); // Prevent the form from submitting
            e.preventDefault();
            const focusedItem = items[currentIndex];
            this.returnFunction(focusedItem);
            return;
        } else {
            return;
        }

        const newItem = items[currentIndex];
        newItem.classList.add(this.suggestionFocusClass);

        // Scroll the new item into view
        newItem.scrollIntoView({ block: 'nearest', inline: 'start' });

        // Focus on the input again
        this.autocompleteElem.focus();
    }

    setSuggestionsMaxHeight() {
        const rect = this.autocompleteElem.getBoundingClientRect();
        this.suggestionsElem.style.maxHeight = `calc(100vh - ${rect.bottom + this.overflowSpace}px)`;
    }

    updateSuggestions(data) {

        this.suggestionsElem.style.display = 'block';
        this.suggestionsElem.innerHTML = this.renderFunction(data);

        // Set max-height of suggestions to prevent overflowing the page, e.g. calc(100vh - 300px);
        if (this.preventOverflow) {
            this.setSuggestionsMaxHeight();
        }
    }
}

export { AutoComplete };