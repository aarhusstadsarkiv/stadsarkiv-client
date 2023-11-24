class AutoComplete {
    constructor(options) {
        
        // Required parameters
        this.autocompleteElem = options.autocompleteElem;
        this.suggestionsElem = options.suggestionsElem;
        this.renderFunction = options.renderFunction;
        this.endpoint = options.endpoint;
        
        // Optional parameters
        this.debounceTimer = options.debounceTimer || 500;
        this.lastInputValue = options.lastInputValue || '';
        this.minInputLength = options.minInputLength || 2;
        this.suggestionFocusClass = options.suggestionFocusClass || 'search-suggestion-focused';
        this.suggestionItemClass = options.suggestionItemClass || 'search-suggestion-item';

        // Debounce timeout ID
        this.timeoutID = null;

        // Bind methods
        this.autocompleteElem.addEventListener('input', this.onInput.bind(this));
        this.autocompleteElem.addEventListener('keydown', this.onKeyDown.bind(this));
        
        // Hide suggestions on resize
        this.hideSuggestions();
        
        // Hide suggestions on resize
        window.addEventListener('resize', this.hideSuggestions.bind(this));
    }

    hideSuggestions() {
        // Hide suggestions on resize and empty the suggestions
        this.suggestionsElem.style.display = 'none';
        this.suggestionsElem.innerHTML = '';
    }

    onInput(event) {

        clearTimeout(this.timeoutID);
        const inputLength = this.autocompleteElem.value.length;
        const inputValue = event.target.value;
        
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
                .then( data => {

                    // FOR TESTING:
                    // 
                    // Just ontil we get some real data
                    // We need to randomize the data and remove some items
                    // to simulate a real search

                    // Sort the data randomly
                    // data.sort(() => Math.random() - 0.5);
                    
                    // // Remove between 1 and 10 items (random)
                    // const random = Math.floor(Math.random() * 10) + 1;
                    
                    // // Remove the random items
                    // data.splice(0, random);
                    
                    this.updateSuggestions(data)
                });
        }, this.debounceTimer);
    }

    /**
     * Check keys pressed in the input field
     */
    onKeyDown(event) {

        const items = this.suggestionsElem.querySelectorAll(`.${this.suggestionItemClass}`);
        if (items.length === 0 && event.key !== 'Escape') return;
    
        if (event.key === 'Escape') {
            event.preventDefault();
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
    
        if (event.key === 'ArrowDown') {
            currentIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
        } else if (event.key === 'ArrowUp') {
            currentIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
        } else if (event.key === 'Enter' && currentIndex !== -1) {
            const focusedItem = items[currentIndex];
            const url = focusedItem.getAttribute('data-url');
            if (url) {
                window.location.href = url;
            }
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
    
    updateSuggestions(data) {

        const inputRect = this.autocompleteElem.getBoundingClientRect();

        // set display to flex
        this.suggestionsElem.style.display = 'block';
        this.suggestionsElem.style.top = `${inputRect.bottom - 80}px`;
        this.suggestionsElem.style.left = `${inputRect.left}px`;
        this.suggestionsElem.innerHTML = this.renderFunction(data);
    }
}

export { AutoComplete };