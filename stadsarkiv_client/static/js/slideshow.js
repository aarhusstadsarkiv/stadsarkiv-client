// Display .prev .next .slide-counter
document.querySelector(".prev").style.display = "block";
document.querySelector(".next").style.display = "block";
document.querySelector(".slide-counter").style.display = "block";

let currentSlideIndex = 0;

showSlide(currentSlideIndex);

function moveSlide(n) {
    showSlide(currentSlideIndex += n);
}

function showSlide(n) {
    let slides = document.getElementsByClassName("slide");
    let currentSlideElem = document.querySelector(".current-slide");
    let totalSlidesElem = document.querySelector(".total-slides");

    // wrap to the start
    if (n >= slides.length) {
        currentSlideIndex = 0;
    }

    // wrap to the end
    if (n < 0) {
        currentSlideIndex = slides.length - 1;
    }

    // Hide all slides
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    // Display the current slide
    slides[currentSlideIndex].style.display = "block";

    // Update the slide counter
    // +1 since we want to display from 1..n instead of 0..n-1
    currentSlideElem.textContent = currentSlideIndex + 1;
    totalSlidesElem.textContent = slides.length;
}

// Add auto slide show
const SECONDS = 15;
let autoSlideShow = setInterval(function () {
    moveSlide(1);
}, 1000 * SECONDS);

// Click events
const prev = document.querySelector(".prev");
const next = document.querySelector(".next");

prev.addEventListener("click", function (event) {
    clearInterval(autoSlideShow);
    event.preventDefault();
    moveSlide(-1);
});

next.addEventListener("click", function (event) {
    clearInterval(autoSlideShow);
    event.preventDefault();
    moveSlide(1);
});

// Keyboard events
document.addEventListener("keydown", function (event) {
    if (event.key === "ArrowLeft") {
        clearInterval(autoSlideShow);
        event.preventDefault();
        moveSlide(-1);
    } else if (event.key === "ArrowRight") {
        clearInterval(autoSlideShow);
        event.preventDefault();
        moveSlide(1);
    }
});

export { }
