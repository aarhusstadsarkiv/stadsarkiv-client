/**
 * function that serializes a js error
 */
function serializeError(error, customMessage) {

    // Split the stack into an array of lines

    // Default custom message is 'JS error'
    if (!customMessage) {
        customMessage = 'JS error';
    }
    return {
        customMessage: customMessage,
        message: error.message,
        name: error.name,
        stack: error.stack,
    };
}

/**
 * 
 * Send the error to the server
 * path /log-js-errord
 */

function asyncLogError(error, customMessage) {
    const errorData = serializeError(error, customMessage);

    // Send as json
    fetch('/error/log', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(errorData),
    }).then(response => {
        // Network error?
        if (!response.ok) {
            console.log("Network response was not ok")
        }

    }).catch(error => {
        // Handle the error
        console.error('There was a problem with the fetch operation:', error);
    });
}

export { asyncLogError }