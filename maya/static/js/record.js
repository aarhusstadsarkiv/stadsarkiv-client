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
 * Swipe left and right on touch devices
 * TODO: Fix swipe on mobile
 */
// let xDown = null;
// let yDown = null;

// function getTouches(evt) {
//     return evt.touches || evt.originalEvent.touches;
// }

// function handleTouchStart(evt) {
//     const firstTouch = getTouches(evt)[0];
//     xDown = firstTouch.clientX;
//     yDown = firstTouch.clientY;
// }

// function handleTouchMove(evt) {
//     if (!xDown || !yDown) {
//         return;
//     }

//     let xUp = evt.touches[0].clientX;
//     let yUp = evt.touches[0].clientY;

//     let xDiff = xDown - xUp;
//     let yDiff = yDown - yUp;

//     if (Math.abs(xDiff) > Math.abs(yDiff)) {
//         if (xDiff > 0) {
//             const nextElem = document.querySelector('.next');
//             if (nextElem) {
//                 nextElem.classList.add('active');
//                 nextElem.click();
//             }
//         } else {
//             const prevElem = document.querySelector('.prev');
//             if (prevElem) {
//                 prevElem.classList.add('active');
//                 prevElem.click();
//             }
//         }
//     }

//     xDown = null;
//     yDown = null;
// }

// document.addEventListener('touchstart', handleTouchStart, false);
// document.addEventListener('touchmove', handleTouchMove, false);