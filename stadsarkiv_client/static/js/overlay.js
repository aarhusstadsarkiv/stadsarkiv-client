/**
 * activateOverlay enhances elements matching a selector to display an overlay with zoom and drag capabilities.
 */
function activateOverlay(selector) {
    // Track the currently opened overlay
    let currentOverlay = null;

    // Setup for each matching element
    document.querySelectorAll(selector).forEach(element => {
        const overlay = element.querySelector('.overlay');
        const image = overlay.querySelector('img');

        if (overlay && image) {
            setupOverlay(overlay, image);
            setupImageClick(element, overlay);
        }
    });

    // Handle the browser's back action to close the overlay
    window.addEventListener('popstate', event => {
        if (currentOverlay && currentOverlay.style.display === 'block') {
            closeOverlay(currentOverlay);
        }
    });

    function setupOverlay(overlay, image) {
        setupZoomAndDrag(image);
        overlay.addEventListener('click', () => {
            if (overlay.style.display === 'block') {
                history.back(); // Triggers popstate event
            }
        });
    }

    function setupImageClick(element, overlay) {
        element.addEventListener('click', () => {
            overlay.style.display = 'block';
            currentOverlay = overlay;
            history.pushState({ overlayOpened: true }, null, null);
        });
    }

    function closeOverlay(overlay) {
        overlay.style.display = 'none';
        currentOverlay = null;
    }

    function setupZoomAndDrag(image) {
        let scale = 1, isDragging = false;
        let startX, startY, posX = 0, posY = 0;

        image.addEventListener('wheel', e => {
            e.preventDefault();
            adjustScale(e.deltaY, image);
        });

        image.addEventListener('mousedown', e => {
            startDragging(e, image);
        });

        document.addEventListener('mousemove', e => {
            if (isDragging) dragImage(e, image);
        });

        document.addEventListener('mouseup', () => {
            if (isDragging) stopDragging(image);
        });

        image.addEventListener('click', e => {
            e.stopPropagation(); // Prevent triggering click on the underlying elements
        });

        function adjustScale(deltaY, image) {
            const delta = deltaY > 0 ? -0.1 : 0.1;
            scale = Math.max(.125, Math.min(scale + delta, 4));
            updateTransform(image);
        }

        function startDragging(e, image) {
            isDragging = true;
            startX = e.clientX - posX;
            startY = e.clientY - posY;
            image.style.cursor = 'grabbing';
        }

        function dragImage(e, image) {
            e.preventDefault();
            posX = e.clientX - startX;
            posY = e.clientY - startY;
            updateTransform(image);
        }

        function stopDragging(image) {
            isDragging = false;
            image.style.cursor = 'grab';
        }

        function updateTransform(image) {
            image.style.transform = `translate(${posX}px, ${posY}px) scale(${scale})`;
        }
    }
}

export { activateOverlay };
