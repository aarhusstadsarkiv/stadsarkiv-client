import { Events } from '/static/js/events.js';
import { Flash } from '/static/js/flash.js';

// Function to save the state of the tree to local storage
function saveTree(event) {

    event.preventDefault();

    const openFacets = [];
    const summaryElements = document.querySelectorAll('.facets details summary');

    summaryElements.forEach(summaryElement => {
        if (summaryElement.parentElement.open) {
            const dataId = summaryElement.getAttribute('data-id');
            openFacets.push(dataId);
        }
    });

    localStorage.setItem('treeState', JSON.stringify(openFacets));
}

// Function to expand the tree based on the saved state from local storage
function expandTree() {
    const openFacets = JSON.parse(localStorage.getItem('treeState'));
    if (openFacets && openFacets.length) {
        const summaryElements = document.querySelectorAll('.facets details summary');
        summaryElements.forEach(summaryElement => {
            const dataId = summaryElement.getAttribute('data-id');
            if (openFacets.includes(dataId)) {
                summaryElement.parentElement.open = true;
            }
        });
    }
}

/**
 * Check if a string is a valid date
 */
function isValidDate(dateString) {
    // Parse the input string as yyyy-mm-dd
    var dateParts = dateString.split("-");
    var year = parseInt(dateParts[0], 10);
    var month = parseInt(dateParts[1], 10);
    var day = parseInt(dateParts[2], 10);

    // Create a new Date object using the parsed values
    var date = new Date(year, month - 1, day);

    // Check if the parsed date is valid
    return (
        date.getFullYear() === year &&
        date.getMonth() === month - 1 &&
        date.getDate() === day
    );
}

/**
 * Search form submit event
 */
let searchDateElem = document.getElementById('search-date');
searchDateElem.addEventListener('submit', function (event) {
    event.preventDefault();

    let fromYear = document.getElementById('from-year').value;
    let fromMonth = document.getElementById('from-month').value || '01';
    let fromDay = document.getElementById('from-day').value || '01';
    let toYear = document.getElementById('to-year').value;
    let toMonth = document.getElementById('to-month').value || '12';
    let toDay = document.getElementById('to-day').value || '31';

    if (!fromYear && !toYear) {
        Flash.setMessage('Du skal indtaste en datoer mellem 1200 og aktuel data', 'error');
        return;
    }

    // One date must be valid now
    let fromDate = `${fromYear}-${fromMonth}-${fromDay}`;
    let toDate = `${toYear}-${toMonth}-${toDay}`;

    if (toYear && !isValidDate(toDate)) {
        Flash.setMessage('Til dato er ikke gyldig', 'error');
        return;
    }

    if (fromYear && !isValidDate(fromDate)) {
        Flash.setMessage('Fra dato er ikke gyldig', 'error');
        return;
    }

    // Redirect to new url
    let url = window.location.href;

    // Add date_from and date_to to url
    let urlParams = new URLSearchParams(window.location.search);
    if (isValidDate(fromDate)) {
        urlParams.set('date_from', `${fromYear}${fromMonth}${fromDay}`);
    }
    if (isValidDate(toDate)) {
        urlParams.set('date_to', `${toYear}${toMonth}${toDay}`);
    }

    // Save the tree state
    saveTree(event);

    window.location.href = url.split('?')[0] + '?' + urlParams.toString();
})

/**
 * Ensure only numbers can be entered in the date fields
 */
Events.addEventListenerMultiple('#search-date > input', 'input', function (e) {
    let input = e.target;
    input.value = input.value.replace(/\D/g, '');
});

/**
 * Expand tree based on saved state
 */

function searchEvents() {

    try {

        document.addEventListener('DOMContentLoaded', function (event) {
            // Expand the tree based on the saved state
            console.log("Loading")
            expandTree();
        })

        // 'beforeunload' will not work when e.g. searching for /search to /search?date_from=20200101
        // Instead we check all links
        window.addEventListener('click', function (event) {

            if (event.target.tagName === 'A') {
                event.preventDefault();
                saveTree(event);
                window.location.href = event.target.href;
            }
        })

        // Also add event listener to search form with id 'search-date'
        let searchElem = document.getElementById('search');
        searchElem.addEventListener('submit', function (event) {
            saveTree(event);
            searchElem.submit();
        })

        // The search-date form is handled in the above.


    } catch (error) {
        // unset local storage if it fails. The tree may be updated and the saved state may be invalid
        localStorage.removeItem('treeState');
        console.log(error);
    }
}

export { searchEvents }
