
const imageContainer = document.querySelector(".horizontal-slider .image-container");
const images = Array.from(document.querySelectorAll(".horizontal-slider .image-item"));

function getVisibleImageIndexes() {
    let containerRect = imageContainer.getBoundingClientRect();
    let visibleIndexes = [];

    images.forEach((img, index) => {
        let imgRect = img.getBoundingClientRect();
        let visibleWidth = Math.min(imgRect.right, containerRect.right) - Math.max(imgRect.left, containerRect.left);
        let visibilityRatio = visibleWidth / imgRect.width;

        if (visibilityRatio >= 1) {
            visibleIndexes.push(index);
        }
    });

    return visibleIndexes;
}

function scrollByImage(direction) {
    let visibleIndexes = getVisibleImageIndexes();
    let targetIndex;
    
    // Determine which image to scroll to next
    if (direction === "left") {
        targetIndex = visibleIndexes[0] - 1; // Move to the leftmost previous image
        if (targetIndex < 0) {
            targetIndex = images.length - 1; // Loop back to the last image
        }
    } else {
        // Scroll to the next image to the right
        targetIndex = visibleIndexes[visibleIndexes.length - 1] + 1;
        if (targetIndex >= images.length) {
            targetIndex = 0; // Loop back to the first image
        }
    }

    let left = 0;

    // Ensure that the targetIndex is within valid bounds
    if (targetIndex >= 0 && targetIndex < images.length) {
        let target = images[targetIndex];

        console.log(target)

        if (direction === "left") {
            left = target.offsetLeft - imageContainer.offsetLeft;
            imageContainer.scrollTo({
                left: left,
                behavior: 'auto'
            });
        } else {
            left = target.offsetLeft + target.offsetWidth - imageContainer.offsetWidth; 
            imageContainer.scrollTo({
                left: left,
                behavior: 'auto'
            });
        }

        localStorage.setItem("left", left);
    }
}

const arrowLeft = document.querySelector(".horizontal-slider .arrow-left-container");
const arrowRight = document.querySelector(".horizontal-slider .arrow-right-container");

function setDisabled() {

    // wait for the scroll to finish
    setTimeout(() => {
        // Set initial disabled on 'arrow-right-container' if first image is visible
        if (getVisibleImageIndexes().includes(0)) {
            arrowLeft.classList.add("disabled");
        } else {
            arrowLeft.classList.remove("disabled");
        }

        // Set initial disabled on 'arrow-right-container' if last image is visible
        if (getVisibleImageIndexes().includes(images.length - 1)) {
            arrowRight.classList.add("disabled");
        } else {
            arrowRight.classList.remove("disabled");
        }
    }, 10);
}

arrowLeft.addEventListener("click", () => {
    // Check if the left arrow is disabled
    if (arrowLeft.classList.contains("disabled")) {
        return
    }

    scrollByImage("left");
    console.log("Scrolling left done")
    setDisabled();
});

arrowRight.addEventListener("click", (event) => {
    // Check if the right arrow is disabled
    if (arrowRight.classList.contains("disabled")) {
        return
    }

    scrollByImage("right");
    setDisabled();
});


// Scroll left if set
if (localStorage.getItem("left")) {
    imageContainer.scrollTo({
        left: localStorage.getItem("left"),
        behavior: 'auto'
    });
}

// set visibility of .image-container to 'initial' after loading
imageContainer.style.visibility = "initial";

setDisabled();

export { };



// const pointerScroll = (elem) => {
//     let clickedElement = null;
//     let isDragging = false;
//     let startX = 0;

//     const dragStart = (ev) => {
//         elem.setPointerCapture(ev.pointerId);
//         startX = ev.clientX;
//         isDragging = false;
//         clickedElement = ev.target;
//         ev.preventDefault();
//     };

//     const dragEnd = (ev) => {
//         elem.releasePointerCapture(ev.pointerId);

//         if (!isDragging && clickedElement) {
//             let target = clickedElement;

//             // Traverse up to find the closest <a> element
//             while (target && target.tagName !== "A") {
//                 target = target.parentElement;
//             }

//             if (target && target.tagName === "A") {
//                 window.location.href = target.href;
//             }
//         }
//     };

//     const drag = (ev) => {
//         if (elem.hasPointerCapture(ev.pointerId)) {
//             if (Math.abs(ev.clientX - startX) > 5) {
//                 isDragging = true;
//             }
//             elem.scrollLeft -= ev.movementX;
//         }
//     };

//     const preventClickOnDrag = (ev) => {
//         if (isDragging) {
//             ev.stopPropagation();
//             ev.preventDefault();
//         }
//     };

//     elem.addEventListener("pointerdown", dragStart);
//     elem.addEventListener("pointerup", dragEnd);
//     elem.addEventListener("pointermove", drag);
//     elem.addEventListener("click", preventClickOnDrag, true); // Capture click events

// };

// document.querySelectorAll(".horizontal-slider .image-container").forEach(pointerScroll);