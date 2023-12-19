class Slideshow {
    constructor(slideshowContainer) {
        this.slideshow = slideshowContainer;
        this.currentSlideIndex = 0;
        this.autoSlideShow = null;
        this.SECONDS = 5;
        this.initSlideshow();
        this.startAutoSlideShow();
    }

    initSlideshow() {
        this.slideshow.querySelector(".prev").style.display = "block";
        this.slideshow.querySelector(".next").style.display = "block";
        this.slideshow.querySelector(".slide-counter").style.display = "block";

        this.showSlide(this.currentSlideIndex);
        this.addEventListeners();
    }

    moveSlide(n) {
        this.showSlide(this.currentSlideIndex += n);
    }

    showSlide(n) {
        let slides = this.slideshow.querySelectorAll(".slide");
        let currentSlideElem = this.slideshow.querySelector(".current-slide");
        let totalSlidesElem = this.slideshow.querySelector(".total-slides");

        if (n >= slides.length) {
            this.currentSlideIndex = 0;
        }

        if (n < 0) {
            this.currentSlideIndex = slides.length - 1;
        }

        for (let slide of slides) {
            slide.style.display = "none";
        }

        slides[this.currentSlideIndex].style.display = "block";
        currentSlideElem.textContent = this.currentSlideIndex + 1;
        totalSlidesElem.textContent = slides.length;
    }

    startAutoSlideShow() {
        this.autoSlideShow = setInterval(() => {
            this.moveSlide(1);
        }, 1000 * this.SECONDS);
    }

    stopAutoSlideShow() {
        clearInterval(this.autoSlideShow);
    }

    addEventListeners() {
        this.slideshow.querySelector(".prev").addEventListener("click", (event) => {
            this.stopAutoSlideShow();
            event.preventDefault();
            this.moveSlide(-1);
        });

        this.slideshow.querySelector(".next").addEventListener("click", (event) => {
            this.stopAutoSlideShow();
            event.preventDefault();
            this.moveSlide(1);
        });

        // document.addEventListener("keydown", (event) => {
        //     if (event.key === "ArrowLeft") {
        //         this.stopAutoSlideShow();
        //         event.preventDefault();
        //         this.moveSlide(-1);
        //     } else if (event.key === "ArrowRight") {
        //         this.stopAutoSlideShow();
        //         event.preventDefault();
        //         this.moveSlide(1);
        //     }
        // });
    }
}

// Usage:
// const slideshows = document.querySelectorAll(".slideshow-container");
function initSlideshows(slideshows) {
    slideshows.forEach(function(slideshow) {
        new Slideshow(slideshow);
    })
}


export { initSlideshows };
