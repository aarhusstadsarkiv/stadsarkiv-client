async function getTranslation(lang) {

    const url = '/static/json/jsoneditor_' + lang + '.json';
    const translation = await fetch(url)
        .then(response => response.json())
        .then(data => {
            return data
        });
    return translation
}

export {getTranslation}