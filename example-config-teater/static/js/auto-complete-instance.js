import { AutoComplete } from '/static/js/auto-complete.js';

function returnFunction(focusedItem) {

    // 'data-url' from focusedItem
    const url = focusedItem.getAttribute('data-url');

    if (url) {
        window.location.href = url;
        return;
    }
}

// Render function for autocomplete
const renderFunction = (data) => {

    // Info if no results
    if (data.length == 0) return `<div class="search-suggestion-info">Ingen forslag. Tryk på søgeknappen for at fritekstsøge i stedet.</div>`;

    // Help text and suggestions
    const suggestionHelp = `<div class="search-suggestion-info">Vælg et forslag nedenfor <strong>eller</strong> tryk på søgeknappen for at fritekstsøge.</div>`;
    
    // Suggestions
    const suggestions = data.map(item => `
        <div class="search-suggestion-item" data-url="/${item.domain}/${item.id}">
            <div>
                <a href="/${item.domain}/${item.id}">${item.display}</a>
            </div>
            <div>${item.sub_display}</div>
        </div>`).join('');

    return `${suggestionHelp} ${suggestions}`;
};

const autocompleteElem = document.querySelector('#q');
const suggestionsElem = document.querySelector('.search-suggestions');

const options = {
    'autocompleteElem': autocompleteElem,
    'suggestionsElem': suggestionsElem,
    'renderFunction': renderFunction,
    'endpoint': `/auto_complete?q=`,
    'minInputLength': 2,
    'suggestionFocusClass': 'search-suggestion-focus',
    'returnFunction': returnFunction,
    'preventOverflow': true,
    'overflowSpace': 10, // In pixels
}

function autoCompleteInit() {
    new AutoComplete(options);
}

export { autoCompleteInit };