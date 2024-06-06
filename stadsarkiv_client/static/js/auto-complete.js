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
        let currentIndex = Array.from(items).findIndex(item => item.classList.contains(this.suggestionFocusClass));
    
        if (items.length === 0) return;
    
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
            e.preventDefault(); // Prevent scrolling the page with arrow keys
    
            // Remove current focus
            if (currentIndex !== -1) {
                items[currentIndex].classList.remove(this.suggestionFocusClass);
            }
    
            if (e.key === 'ArrowDown') {
                currentIndex = (currentIndex + 1) % items.length;
            } else if (e.key === 'ArrowUp') {
                currentIndex = (currentIndex - 1 + items.length) % items.length;
            }

            console.log(items)
            console.log(currentIndex)
    
            // Add new focus
            items[currentIndex].classList.add(this.suggestionFocusClass);
            items[currentIndex].scrollIntoView({ block: 'nearest', inline: 'start' });
        } else if (e.key === 'Enter' && currentIndex !== -1) {
            e.stopPropagation();
            e.preventDefault();
            this.returnFunction(items[currentIndex]);
        } else if (e.key === 'Escape') {
            this.hideSuggestions();
        }
        
        // Keep focus on the input field
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