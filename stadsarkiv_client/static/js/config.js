const Config = {
    api_url: ''
}

function getApiUrl(path) {
    return Config.api_url + path;
}

export { getApiUrl };
