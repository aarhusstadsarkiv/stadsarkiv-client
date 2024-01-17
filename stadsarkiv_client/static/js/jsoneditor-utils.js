async function getTranslation(lang) {

    const url = '/static/json/jsoneditor_' + lang + '.json';
    const translation = await fetch(url)
        .then(response => response.json())
        .then(data => {
            return data
        });
    return translation
}

function showErrorMessages(schema, errors) {

    let messages = []


    for (let i = 0; i < errors.length; i++) {

        const error = errors[i]

        // // Remove root. from error.path e.g root.name.first
        // const field = error.path.split('.').slice(1).join('.')

        // // Remove any '.' and a number from end of field e.g name.0 -> name
        // let fieldCleaned = field
        // if (field.match(/\.\d+$/)) {
        //     fieldCleaned = field.replace(/\.\d+$/, '')
        // }

        // // Split field into parts
        // const fieldParts = fieldCleaned.split('.')

        // // Iterate schema.data.properties and find the final fieldSchema
        // let fieldSchema = schema.data
        // fieldParts.forEach(fieldPart => {
        //     fieldSchema = fieldSchema.properties[fieldPart]
        // });

        // const fieldTitle = fieldSchema.title || error.path
        // const message = "Validerings fejl i feltet " + fieldTitle + ": " + error.message;
        // messages.push(message)

        console.log(errors)

        let message = `Validerings fejl i feltet "${error.path}": ${error.message}`
        messages.push(message)

    };

    if (messages.length > 0) {
        const header = document.querySelector('.je-object__title')

        // Remove old error messages
        const oldErrorMessages = document.querySelectorAll('.error-message')
        oldErrorMessages.forEach(element => {
            element.remove()
        });

        // Add new error messages
        messages.forEach(element => {
            const error_message = document.createElement('div')
            error_message.classList.add('error-message')
            error_message.innerHTML = element
            header.after(error_message)
        });

        // const element = document.querySelector('#editor_holder')

        // element is first h3
        const element = document.querySelector('h3')
        element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
}

async function getEditor(schema) {

    const translation = await getTranslation("da")

    // Initialize the editor with a JSON schema
    const options = {
        theme: 'barebones',
        disable_properties: true,
        disable_collapse: true,
        disable_edit_json: true,
        show_opt_in: false,
        use_default_values: true,
        schema: schema.data,
        // show_errors: 'change',
    }

    /*
            theme: 'barebones',
        disable_properties: true,
        disable_collapse: true,
        disable_edit_json: true,
        show_opt_in: true,
        // use_default_values: true,
        remove_empty_properties: false,
        schema: schema.data,
        */

    JSONEditor.defaults.languages.da = translation
    JSONEditor.defaults.language = "da";

    const editor = new JSONEditor(document.getElementById('editor_holder'), options);
    return editor
}

export { getTranslation, showErrorMessages, getEditor }
