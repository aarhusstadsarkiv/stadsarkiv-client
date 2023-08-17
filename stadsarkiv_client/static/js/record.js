/**
 * Next prev shortcuts for search results displayed on record page
 */
document.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') {
        const prevElem = document.querySelector('.prev');
        if (prevElem) {
            prevElem.classList.add('active'); // Add 'active' class
            prevElem.click();
        }
    } else if (e.key === 'ArrowRight') {
        const nextElem = document.querySelector('.next');
        if (nextElem) {
            nextElem.classList.add('active'); // Add 'active' class
            nextElem.click();
        }
    }
});

/**
 * Simple overlay for record image
 */

let overlayHistoryModified = false;

const recordImage = document.querySelector('.record-image');
if (recordImage) {
    recordImage.addEventListener('click', function () {
        const overlay = document.getElementById('overlay');
        overlay.style.display = 'block';

        // Only modify history if it hasn't been modified before by the overlay
        // Add to history so that the user can use the back button to close the overlay
        if (!overlayHistoryModified) {
            history.pushState({ overlayOpened: true }, null, null);
            overlayHistoryModified = true;
        }
    });
}

const overlay = document.getElementById('overlay');
if (overlay) {
    overlay.addEventListener('click', function () {
        this.style.display = 'none';
        overlayHistoryModified = false; // Reset the flag
    });
}

window.addEventListener('popstate', function (event) {
    const overlay = document.getElementById('overlay');

    // If the overlay is displayed, hide it
    if (overlay.style.display === 'block') {
        overlay.style.display = 'none';
        overlayHistoryModified = false; // Reset the flag
    }
});

export { }