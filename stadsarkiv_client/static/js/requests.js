class Requests {

    /**
     * Post formdata async. Accepts JSON as response
     * 
     * Example:
     * 
     * E.g. Get form data from an form element:
     * 
     * const formElem = document.getElementById('formElem');
     * const formData = new FormData(formElem);
     * 
     * const res = await Requests.asyncPost('/url', formData);
     */
    static async asyncPost(url, formData, method) {
        if (!method) method = 'post'
        const rawResponse = await fetch(url, {
            method: method,
            headers: {
                'Accept': 'application/json',
            },
            body: formData
        }).then(function (response) {
            return response.json()
        }).then(function (response) {
            return response;
        });

        return rawResponse;
    }

    /**
     * POST JSON async. 
     * 
     * Example:
     * 
     * With object: 
     * 
     * let formData = new FormData();
     * formData.append('user_status', 'DELETED');
     * 
     * With JSON:
     * 
     * let formData = {
     *    user_status: 'DELETED'
     * }
     * 
     * const res = await Requests.asyncPostJson(url, formData);
     */
    static async asyncPostJson(url, jsonData, method) {

        // If JSON it not stringified, do it
        if (typeof jsonData !== 'string') {
            jsonData = JSON.stringify(jsonData);
        }

        if (!method) method = 'POST'
        const rawResponse = await fetch(url, {
            method: method,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: jsonData
        }).then(function (response) {
            return response.json()
        }).then(function (response) {
            return response;
        });

        return rawResponse;
    }

    /**
     * Get JSON async
     * 
     * Example:
     * 
     * const res = await Requests.asyncGetJson(url);
     */
    static async asyncGetJson(url, method) {
        if (!method) method = 'GET'
        const rawResponse = await fetch(url, {
            method: method,
            headers: {
                'Accept': 'application/json',
            }
        }).then(function (response) {
            return response.json()
        }).then(function (response) {
            return response;
        });

        return rawResponse;
    }
}

export { Requests }