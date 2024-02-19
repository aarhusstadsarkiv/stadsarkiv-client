/* 

<div class="overlays">
    <!-- a link to open the overlay --> 
    <a href="#overlay-image-1"><img src="/image.jpg"></a>
    
    <!-- the overlay. Notice the data-overlay-id is the same as the link to open the overlay except for the '#' -->
    <div data-overlay-id="overlay-image-1">
        <div class="overlay overlay-hidden">
            <img id="overlay-image" src=/image-large.jpg">
            <!-- close and zoom reset buttons -->
            <div class="overlay-actions">
                <div class="overlay-close"">Close</div>
                <div class="overlay-reset">Reset</div>
            </div>
        </div>
    </div>
</div>  

*/

function activateOverlay(selector) {

    // Check if the selector is valid
    const allOverlays = document.querySelectorAll(selector);
    if (allOverlays.length === 0) {
        return;
    }

    // Initialize all overlays
    allOverlays.forEach(element => {
        const overlay = element.querySelector('.overlay');
        setupSingleOverlay(overlay);
    });

    window.addEventListener('hashchange', checkHash);
    checkHash();
}

function setupSingleOverlay(overlay) {
    const image = overlay.querySelector('img');
    const overlayClose = overlay.querySelector('.overlay-close');
    const overlayReset = overlay.querySelector('.overlay-reset');
    const maxScale = 7;
    const scaleStep = 0.15;

    let scale = 1;
    let isDragging = false;
    let startX;
    let startY;
    let posX = 0;
    let posY = 0;

    overlayClose.addEventListener('click', () => {
        history.back();
    });

    overlayReset.addEventListener('click', () => {
        scale = 1;
        posX = 0;
        posY = 0;
        image.style.transform = `translate(${posX}px, ${posY}px) scale(${scale})`;
    });

    image.addEventListener('wheel', e => {
        const dalta = e.deltaY > 0 ? -scaleStep : scaleStep;
        scale = Math.max(1, Math.min(scale + dalta, maxScale));
        image.style.transform = `translate(${posX}px, ${posY}px) scale(${scale})`;
    });

    image.addEventListener('mousedown', e => {
        isDragging = true;
        startX = e.clientX - posX;
        startY = e.clientY - posY;
    });

    document.addEventListener('mousemove', e => {
        if (isDragging) {
            e.preventDefault();
            posX = e.clientX - startX;
            posY = e.clientY - startY;
            image.style.transform = `translate(${posX}px, ${posY}px) scale(${scale})`;
        }
    });

    document.addEventListener('mouseup', () => {
        if (isDragging) {
            isDragging = false;
        }
    });
}



function checkHash() {
    const overlayIds = document.querySelectorAll('[data-overlay-id]')
    overlayIds.forEach(element => {
        const overlay = element.querySelector('.overlay');
        if (window.location.hash === '#' + element.dataset.overlayId) {
            overlay.style.display = 'block';
        } else {
            overlay.style.display = 'none';
        }
    });
}

export { activateOverlay };
