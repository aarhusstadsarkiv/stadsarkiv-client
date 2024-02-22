class Requests {

    /**
     * Post formdata async. Accepts JSON as response
     */
    static async asyncPost(url, formData, method) {
        if (!method) method = 'post'
        const rawResponse = await fetch(url, {
            method: 'post',
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
     * Post JSON async. Accepts JSON as response
     */
    static async asyncPostJson(url, formData, method) {
        if (!method) method = 'POST'
        const rawResponse = await fetch(url, {
            method: method,
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: formData
        }).then(function (response) {
            return response.json()
        }).then(function (response) {
            return response;
        });

        return rawResponse;
    }

    static async asyncGetJson(url) {
        const rawResponse = await fetch(url, {
            method: 'get',
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