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

    // reverse errors
    errors = errors.reverse()
    for (let i = 0; i < errors.length; i++) {

        const error = errors[i]

        // Remove root. from error.path e.g root.name.first
        const field = error.path.split('.').slice(1).join('.')
        
        // Remove any '.' and a number from end of field e.g name.0 -> name
        let fieldCleaned = field
        if (field.match(/\.\d+$/)) {
            fieldCleaned = field.replace(/\.\d+$/, '')
        }            
        
        // Split field into parts
        const fieldParts = fieldCleaned.split('.')

        // Iterate schema.data.properties and find the final fieldSchema
        let fieldSchema = schema.data
        fieldParts.forEach(fieldPart => {
            fieldSchema = fieldSchema.properties[fieldPart]
        });

        const fieldTitle = fieldSchema.title || error.path
        const message = "Validerings fejl i feltet " + fieldTitle + ": " + error.message;

        const element = document.querySelector(`[data-schemapath="root.${field}"]`)
        element.scrollIntoView({ behavior: 'smooth', block: 'start' })

        Flash.setMessage(message, 'error')
        
    };
}

export {getTranslation, parseErrors}