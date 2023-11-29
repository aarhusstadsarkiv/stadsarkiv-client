import { Events } from '/static/js/events.js';
import { Flash } from '/static/js/flash.js';

// Function to save the state of the tree to local storage
function saveTree() {

    const openFacets = [];
    const detailsElements = document.querySelectorAll('.container-left .facets details');
    detailsElements.forEach(detailElement => {
        if (detailElement.open) {
            const dataId = detailElement.getAttribute('data-id');
            openFacets.push(dataId);
        }
    });

    localStorage.setItem('treeState', JSON.stringify(openFacets));
}

function collapseTree() {
    const detailsElements = document.querySelectorAll('.container-main-facets .facets details');
    detailsElements.forEach(detailElement => {
        detailElement.open = false;
    });
}

// Function to expand the tree based on the saved state from local storage
function expandTree() {
    const openFacets = JSON.parse(localStorage.getItem('treeState'));
    if (openFacets && openFacets.length) {
        const detailElements = document.querySelectorAll('.container-left .facets details');
        detailElements.forEach(detailElement => {
            const dataId = detailElement.getAttribute('data-id');
            if (openFacets.includes(dataId)) {
                detailElement.open = true;
            }
        });
    }
}

/**
 * Check if a string is a valid date
 */
function isValidDate(dateString) {

    // Parse the input string as yyyy-mm-dd
    const dateParts = dateString.split("-");
    const year = parseInt(dateParts[0], 10);
    const month = parseInt(dateParts[1], 10);
    const day = parseInt(dateParts[2], 10);

    // Create a new Date object using the parsed values
    const date = new Date(year, month - 1, day);

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
function onSearchDateEvent(dateFormClass) {
    const searchDateElem = document.querySelector(dateFormClass);
    if (!searchDateElem) {
        return;
    }

    searchDateElem.addEventListener('submit', function (event) {
        event.preventDefault();

        const fromYear = document.querySelector(`${dateFormClass} .from-year`).value;
        const fromMonth = document.querySelector(`${dateFormClass} .from-month`).value || '01';
        const fromDay = document.querySelector(`${dateFormClass} .from-day`).value || '01';
        const toYear = document.querySelector(`${dateFormClass} .to-year`).value;
        const toMonth = document.querySelector(`${dateFormClass} .to-month`).value || '12';
        const toDay = document.querySelector(`${dateFormClass} .to-day`).value || '31';

        if (!fromYear && !toYear) {
            Flash.setMessage('Du skal indtaste en dato mellem 1200 og aktuel data', 'error');
            return;
        }

        // One date has been entered now
        const fromDate = `${fromYear}-${fromMonth}-${fromDay}`;
        const toDate = `${toYear}-${toMonth}-${toDay}`;

        if (toYear && !isValidDate(toDate)) {
            Flash.setMessage('Til dato er ikke gyldig', 'error');
            return;
        }

        if (fromYear && !isValidDate(fromDate)) {
            Flash.setMessage('Fra dato er ikke gyldig', 'error');
            return;
        }

        // Redirect to new url and add date_from and date_to to url
        const url = window.location.href;
        const urlParams = new URLSearchParams(window.location.search);
        if (isValidDate(fromDate)) {
            urlParams.set('date_from', `${fromYear}${fromMonth}${fromDay}`);
        }
        if (isValidDate(toDate)) {
            urlParams.set('date_to', `${toYear}${toMonth}${toDay}`);
        }

        saveTree();
        window.location.href = url.split('?')[0] + '?' + urlParams.toString();
    });
}

/**
 * Expand tree based on saved state
 */
function searchEvents() {

    try {

        // Two date search forms on search page
        onSearchDateEvent('.search-date');
        onSearchDateEvent('.search-date-main');

        // Ensure only numbers can be entered in the date fields
        Events.addEventListenerMultiple('.search-date > input', 'input', function (e) {
            const input = e.target;
            input.value = input.value.replace(/\D/g, '');
        });

        Events.addEventListenerMultiple('.search-date-main > input', 'input', function (e) {
            const input = e.target;
            input.value = input.value.replace(/\D/g, '');
        });

        // Expand the tree based on the saved state
        document.addEventListener('DOMContentLoaded', function (event) {
            // Check if tree threshold has been reached
            const maxWidth = 992;
            const width = window.innerWidth;
            if (width > maxWidth) {
                expandTree();
            }
        })

        // 'beforeunload' will not work when e.g. searching for /search to /search?date_from=20200101
        // Instead we check all links
        const searchLinks = document.querySelectorAll('.search-link, a');
        searchLinks.forEach(searchLink => {
            searchLink.addEventListener('click', function (event) {
                event.preventDefault();
                saveTree();

                // Check if _blank is set
                const target = searchLink.getAttribute('target');
                if (target == '_blank') {
                    window.open(searchLink.href, '_blank');
                } else {
                    window.location.href = searchLink.href;
                }
            })
        })

        // Also add event listener to search form with id 'search-date'
        const searchElem = document.getElementById('search');
        searchElem.addEventListener('submit', function (event) {
            event.preventDefault();
            saveTree();
            searchElem.submit();
        })

        const selectSize = document.querySelector('.select-size');
        selectSize.addEventListener('change', function () {
            saveTree();
            document.getElementById('size').submit();
        });

        const selectSort = document.querySelector('.select-sort');
        selectSort.addEventListener('change', function () {

            const selectedValue = selectSort.value;
            if (selectedValue == 'date_to') {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'direction';
                input.value = 'desc';
                document.getElementById('sort').appendChild(input);
            }

            if (selectedValue == 'date_from') {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'direction';
                input.value = 'asc';
                document.getElementById('sort').appendChild(input);
            }

            saveTree();
            document.getElementById('sort').submit();
        });

    } catch (error) {
        // unset local storage if it fails. 
        // The tree may be updated and the saved state may be invalid
        localStorage.removeItem('treeState');
        console.log(error);
    }
}

export { searchEvents }
