/**
 * activateOverlay takes a selector as argument.
 * This selector needs a 
 * .overlay child element containing an image
 * img element.  
 */
function activateOverlay(selector) {
    // Track the currently opened overlay
    let currentOverlay = null;

    // Find all elements matching the selector
    const elements = document.querySelectorAll(selector);
    elements.forEach(element => {
        const overlay = element.querySelector('.overlay');
        const image = element.querySelector('img');
        if (image && overlay) {
            image.addEventListener('click', function () {
                overlay.style.display = 'block';
                currentOverlay = overlay;
                // Add to history so that the user can use the back button to close the overlay
                history.pushState({ overlayOpened: true }, null, null);
            });
        }

        if (overlay) {
            overlay.addEventListener('click', function () {
                if (overlay.style.display === 'block') {
                    // This will execute the popstate event listener
                    history.back();
                }
            });
        }
    });

    window.addEventListener('popstate', function (event) {
        console.log("popstate");
        // If an overlay is displayed, hide it
        if (currentOverlay && currentOverlay.style.display === 'block') {
            currentOverlay.style.display = 'none';
            currentOverlay = null; // Reset the current overlay
        }
    });
}

export { activateOverlay }