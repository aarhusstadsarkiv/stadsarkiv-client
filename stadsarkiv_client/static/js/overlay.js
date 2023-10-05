/**
 * Simple overlay for record image
 */

let overlayHistoryModified = false;


/**
 * ActivateOverlay takes a selector as argument.
 * This selector needs a 
 * .overlay child element containing a image
 * img element. 
 * 
 * 
 */
function activateOverlay(selector) {

    const overlaySelector = `${selector} > .overlay`;
    const overlay = document.querySelector(overlaySelector);

    // '.record-representation'
    const recordImageSelector = `${selector} > img`;
    const recordImage = document.querySelector(recordImageSelector);
    if (recordImage) {
        recordImage.addEventListener('click', function () {

            overlay.style.display = 'block';

            // Only modify history if it hasn't been modified before by the overlay
            // Add to history so that the user can use the back button to close the overlay
            if (!overlayHistoryModified) {
                history.pushState({ overlayOpened: true }, null, null);
                overlayHistoryModified = true;
            }
        });
    }

    if (overlay) {
        overlay.addEventListener('click', function () {
            this.style.display = 'none';
            overlayHistoryModified = false; // Reset the flag
        });
    }

    window.addEventListener('popstate', function (event) {

        // If the overlay is displayed, hide it
        if (overlay.style.display === 'block') {
            overlay.style.display = 'none';
            overlayHistoryModified = false; // Reset the flag
        }
    });
}

export { activateOverlay }