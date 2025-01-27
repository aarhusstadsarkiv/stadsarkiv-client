/**
 * Simple Requests module for 
 * Posting a FormData object or a JSON object
 * Or getting JSON from a URL
 */

class Requests {

    /**
     * Post FormData async. Accepts JSON as response
     * 
     * Example (use in try catch block):
     * 
     * const formElem = document.getElementById('formElem');
     * const formData = new FormData(formElem);
     * 
     * const res = await Requests.asyncPost('/url', formData);
     * 
     */
    static async asyncPost(url, formData, method = 'POST') {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Accept': 'application/json',
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error(`POST request failed: ${response.status} ${response.statusText}`);
        }

        return response.json();
    }

    /**
     * POST JSON async. Send a JSON object or a JSON string.
     * 
     * Example (use in try catch block):
     * 
     * let jsonData = { user_status: 'DELETED' };
     * const res = await Requests.asyncPostJson(url, jsonData);
     * 
     */
    static async asyncPostJson(url, jsonData = {}, method = 'POST') {
        if (typeof jsonData !== 'string') {
            jsonData = JSON.stringify(jsonData);
        }

        const response = await fetch(url, {
            method: method,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: jsonData
        });

        if (!response.ok) {
            throw new Error(`POST request failed: ${response.status} ${response.statusText}`);
        }

        return response.json();
    }

    /**
     * Get JSON async.

     * Example (use in try catch block):
     *
     * const res = await Requests.asyncGetJson(url);
     */
    static async asyncGetJson(url, method='GET') {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Accept': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`GET request failed: ${response.status} ${response.statusText}`);
        }

        return response.json();
    }
}

export { Requests }