import { asyncLogError } from "/static/js/error.js";

const images = document.querySelectorAll('img');

images.forEach(function(img) {
    img.onerror = function() {

        // If image attribute loading equals "lazy" loaded ignore it
        if (img.getAttribute('loading') === 'lazy') {
            return;
        }
        
        console.log('Image failed to load:', img.src);

    };
});
