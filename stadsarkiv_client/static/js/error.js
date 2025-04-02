/**
 * function that serializes the error
 */
function serializeError(error) {
    // Note: error_type, error_code, error_url are options in the python logger
    // May use them at some point 
    let data = {
        message: error.message,
        exception: error.stack,
    };

    return data;
}

/**
 * Send the error to the server
 * If the error is a JS error it has a stack trace and a message
 * Otherwise you may compose the error object yourself
 */
function asyncLogError(error) {

    const errorData = serializeError(error);

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