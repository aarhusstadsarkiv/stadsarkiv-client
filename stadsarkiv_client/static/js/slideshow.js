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


document.querySelector(".prev").addEventListener("click", function(event) {
    event.preventDefault();
    moveSlide(-1);
})

document.querySelector(".next").addEventListener("click", function(event) {
    event.preventDefault();
    moveSlide(1);
})

export {  }
