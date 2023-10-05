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


export { }