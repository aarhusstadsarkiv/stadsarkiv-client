import { Flash } from "/static/js/flash.js";

async function getTranslation(lang) {

    const url = '/static/json/jsoneditor_' + lang + '.json';
    const translation = await fetch(url)
        .then(response => response.json())
        .then(data => {
            return data
        });
    return translation
}

function parseErrors(schema, errors) {
    errors.forEach(error => {

        // Get field title from json schema
        console.log(error)
        
        // Remove root. from error.path
        const field = error.path.split('.').slice(1).join('.')
        
        // Split field into parts
        const fieldParts = field.split('.')

        // Go into schema.data.properties and find the correct field
        let fieldSchema = schema.data

        fieldParts.forEach(field_part => {
            fieldSchema = fieldSchema.properties[field_part]
        });

        const fieldTitle = fieldSchema.title || error.path
        const message = "Validerings fejl i feltet " + fieldTitle + ": " + error.message;

        const element = document.querySelector(`[data-schemapath="root.${field}"]`)
        element.scrollIntoView({ behavior: 'smooth', block: 'start' })

        Flash.setMessage(message, 'error')
    });
}

export {getTranslation, parseErrors}