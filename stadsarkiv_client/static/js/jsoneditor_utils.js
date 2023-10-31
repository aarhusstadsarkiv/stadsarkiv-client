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

        // Remove root. from error.path e.g root.name.first
        const field = error.path.split('.').slice(1).join('.')
        
        // Split field into parts
        const fieldParts = field.split('.')

        // Iterate schema.data.properties and find the final fieldSchema
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