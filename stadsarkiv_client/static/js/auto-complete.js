class AutoComplete {
    constructor(element, suggestionsElem, renderFunction) {
        this.element = element;
        this.suggestionsElem = suggestionsElem;
        this.renderFunction = renderFunction;
        this.debounceTimer = null;
        this.element.addEventListener('input', this.onInput.bind(this));
        this.element.addEventListener('keydown', this.onKeyDown.bind(this));
        this.lastInputValue = '';
        window.addEventListener('resize', this.resize.bind(this));
        this.resize();

    }

    resize() {
        // Hide suggestions on resize
        this.suggestionsElem.style.display = 'none';
        this.suggestionsElem.innerHTML = '';
    }

    onInput(event) {

        clearTimeout(this.debounceTimer);
        const inputLength = this.element.value.length;
        const inputValue = event.target.value;
        
        if (inputLength < 2 ) {
            this.suggestionsElem.style.display = 'none';
            this.suggestionsElem.innerHTML = '';
            return;
        }

        // Do not fetch if the input value is the same as the last input value
        if (inputValue === this.lastInputValue) return;
        this.lastInputValue = inputValue;

        this.debounceTimer = setTimeout(() => {
            fetch(`/static/json/auto-suggest.json?q=${inputValue}`)
                .then(response => response.json())
                .then( data => {

                    // Just ontil we get some real data
                    // We need to randomize the data and remove some items
                    // to simulate a real search

                    // Sort the data randomly
                    data.sort(() => Math.random() - 0.5);
                    
                    // Remove between 1 and 10 items (random)
                    const random = Math.floor(Math.random() * 10) + 1;
                    
                    // Remove the random items
                    data.splice(0, random);
                    
                    this.updateSuggestions(data)
                });
        }, 500);
    }

    /**
     * Check if ArrowDown or ArrowUp or Enter is pressed
     */
    onKeyDown(event) {

        const items = this.suggestionsElem.querySelectorAll('.search-suggestion-item');
        if (items.length === 0) return;

        let currentIndex = -1;
        items.forEach((item, index) => {
            if (item.classList.contains('search-suggestion-focused')) {
                currentIndex = index;
                item.classList.remove('search-suggestion-focused');
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
        newItem.classList.add('search-suggestion-focused');

        // Focus on the input again
        this.element.focus();
        event.preventDefault();
    }


    updateSuggestions(data) {

        const inputRect = this.element.getBoundingClientRect();

        // set display to flex
        this.suggestionsElem.style.display = 'flex';
        this.suggestionsElem.style.top = `${inputRect.bottom - 80}px`;
        this.suggestionsElem.style.left = `${inputRect.left}px`;
        this.suggestionsElem.innerHTML = this.renderFunction(data);
    }
}

export { AutoComplete };