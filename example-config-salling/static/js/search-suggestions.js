
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
    } else {
        // Scroll to the next image to the right
        targetIndex = visibleIndexes[visibleIndexes.length - 1] + 1;
    }

    // Ensure that the targetIndex is within valid bounds
    if (targetIndex >= 0 && targetIndex < images.length) {
        let target = images[targetIndex];
        console.log(target)

        if (direction === "left") {
            imageContainer.scrollTo({
                left: target.offsetLeft - imageContainer.offsetLeft,
                behavior: 'instant'
            });
        } else {
            imageContainer.scrollTo({
                left: target.offsetLeft + target.offsetWidth - imageContainer.offsetWidth,
                behavior: 'instant'
            });
        }
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
    scrollByImage("left");
    console.log("Scrolling left done")
    setDisabled();
});

arrowRight.addEventListener("click", () => {
    scrollByImage("right");
    setDisabled();
});

setDisabled();

const pointerScroll = (elem) => {
    let clickedElement = null;
    let isDragging = false;
    let startX = 0;

    const dragStart = (ev) => {
        elem.setPointerCapture(ev.pointerId);
        startX = ev.clientX;
        isDragging = false;
        clickedElement = ev.target; // Store the initially clicked element
        ev.preventDefault(); // Prevent default image dragging
    };

    const dragEnd = (ev) => {
        elem.releasePointerCapture(ev.pointerId);

        if (!isDragging && clickedElement) {
            let target = clickedElement;

            // Traverse up to find the closest <a> element
            while (target && target.tagName !== "A") {
                target = target.parentElement;
            }

            if (target && target.tagName === "A") {
                window.location.href = target.href;
            }
        }
    };

    const drag = (ev) => {
        if (elem.hasPointerCapture(ev.pointerId)) {
            if (Math.abs(ev.clientX - startX) > 5) {
                isDragging = true;
            }
            elem.scrollLeft -= ev.movementX;
        }
    };

    const preventClickOnDrag = (ev) => {
        if (isDragging) {
            ev.stopPropagation();
            ev.preventDefault(); // Prevent click from triggering navigation
        }
    };

    elem.addEventListener("pointerdown", dragStart);
    elem.addEventListener("pointerup", dragEnd);
    elem.addEventListener("pointermove", drag);
    elem.addEventListener("click", preventClickOnDrag, true); // Capture click events

};

document.querySelectorAll(".horizontal-slider .image-container").forEach(pointerScroll);

export { };