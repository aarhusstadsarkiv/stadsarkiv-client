class Requests {

    /**
     * Post formdata async. Accepts JSON as response
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
     * Post JSON string or JS object that can be stringified. 
     * Accepts JSON as response
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