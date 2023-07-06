import { Events } from '/static/js/events.js';
import { Flash } from '/static/js/flash.js';

// Function to save the state of the tree to local storage
function saveTree() {
    const detailsElements = document.querySelectorAll('details');
    const state = [];

    detailsElements.forEach((detailsElement) => {
        const isOpen = detailsElement.hasAttribute('open');
        state.push(isOpen);
    });

    localStorage.setItem('treeState', JSON.stringify(state));
}

// Function to expand the tree based on the saved state from local storage
function expandTree() {
    const savedState = localStorage.getItem('treeState');

    if (savedState) {
        const state = JSON.parse(savedState);
        const detailsElements = document.querySelectorAll('details');

        detailsElements.forEach((detailsElement, index) => {
            const isOpen = state[index];
            if (isOpen) {
                detailsElement.setAttribute('open', 'true');
            } else {
                detailsElement.removeAttribute('open');
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
 * Search form
 * Check if dates are valid and add hidden date inputs to form
 * formatted to yyyymmdd
 */
Events.addEventListenerMultiple('#search-date', 'submit', function (e) {
    e.preventDefault();
    let fromYear = document.getElementById('from-year').value;
    let fromMonth = document.getElementById('from-month').value || '01';
    let fromDay = document.getElementById('from-day').value || '01';

    // let currentYear = new Date().getFullYear();

    let toYear = document.getElementById('to-year').value;
    let toMonth = document.getElementById('to-month').value || '12';
    let toDay = document.getElementById('to-day').value || '31';

    if (!fromYear && !toYear) {
        Flash.setMessage('Du skal indtaste en dato mellem 1200 og aktuel data', 'error');
        return;
    }

    // One date must be valid now
    let fromDate = `${fromYear}-${fromMonth}-${fromDay}`;
    let toDate = `${toYear}-${toMonth}-${toDay}`;

    if (isValidDate(fromDate)) {
        // add hidden input to form
        let input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'date_from';
        input.value = `${fromYear}${fromMonth}${fromDay}`;
        document.getElementById('search-date').appendChild(input);
    } else {
        if (fromYear) {
            Flash.setMessage('Fra dato er ikke gyldig', 'error');
            return;
        }
    }

    if (toYear && isValidDate(toDate)) {
        // add hidden input to form
        let input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'date_to';
        input.value = `${toYear}${toMonth}${toDay}`;;
        document.getElementById('search-date').appendChild(input);
    } else {
        if (toYear) {
            Flash.setMessage('Til dato er ikke gyldig', 'error');
            return;
        }
    }

    // Set disabled on existing inputs to prevent them from being submitted
    document.getElementById('from-year').disabled = true;
    document.getElementById('from-month').disabled = true;
    document.getElementById('from-day').disabled = true;
    document.getElementById('to-year').disabled = true;
    document.getElementById('to-month').disabled = true;
    document.getElementById('to-day').disabled = true;

    // Submit new form to current url with new hidden inputs
    document.getElementById('search-date').submit();

});

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
document.addEventListener('DOMContentLoaded', () => {
    try {
        expandTree();
        window.addEventListener('beforeunload', saveTree);

    } catch (error) {
        // unset local storage if it fails. The tree may be updated and the saved state may be invalid
        localStorage.removeItem('treeState');
        console.log(error);
    }
});


let Search = {};

export { Search }
