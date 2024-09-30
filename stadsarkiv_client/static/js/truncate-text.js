/**
 * Function that truncates or restores text content of elements
 * @param {*} elements 
 * @param {*} maxLength 
 * @param {*} shouldTruncate 
 */

function truncateText(elements, maxLength, shouldTruncate) {
    for (let i = 0; i < elements.length; i++) {
        let text = elements[i].textContent;
        
        if (shouldTruncate) {
            // Store the original text
            if (!elements[i].getAttribute('data-original-text')) {
                elements[i].setAttribute('data-original-text', text);
            }

            if (text.length > maxLength) {

                let truncated = text.substring(0, maxLength);
                let lastSpaceIndex = truncated.lastIndexOf(" ");
                
                if (lastSpaceIndex > 0) {
                    truncated = truncated.substring(0, lastSpaceIndex);
                }
                
                elements[i].textContent = truncated + "...";
            }
        }
        // If shouldTruncate is false, restore the original text
        else {
            let originalText = elements[i].getAttribute('data-original-text');
            if (originalText) {
                elements[i].textContent = originalText;
            }
        }
    }
}

export { truncateText };
