import { asyncLogError } from "/static/js/error.js";

const images = document.querySelectorAll('img');
images.forEach((img) => {
    img.onerror = async () => {

        // If image attribute loading equals "lazy" loaded ignore it
        if (img.getAttribute('loading') === 'lazy') {
            return;
        }

        let error = new Error("Missing Image Error");

        // Set current url 
        error.error_url = window.location.href;
        error.error_code = 404;
        error.error_type = "MissingImageError";

        console.log(error);
        asyncLogError(error);

    };
});
