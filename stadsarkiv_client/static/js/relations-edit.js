// import { html, render } from 'https://cdn.jsdelivr.net/npm/lit-html/lit-html.js';
import { html, render } from '/static/js/lit-html.js';
import { AutoComplete } from '/static/js/auto-complete.js';
import { Flash } from '/static/js/flash.js';
import { Requests } from "/static/js/requests.js";

let relations; 
let resourceOriginal;
let state = {
    // Show form for relation
    formShow: null,
    // If edit mode is on
    editEnabled: false,

}
let currentAutoCompleteData = []

// Render the autocomplete suggestions as HTML
const renderFunction = (data) => {

    currentAutoCompleteData = data;

    // Info if no results
    if (data.length == 0) return `<div class="search-suggestion-info">Ingen forslag. Tryk på søgeknappen for at fritekstsøge i stedet.</div>`;

    // Help text and suggestions
    const suggestionHelp = `<div class="search-suggestion-info">Vælg et forslag nedenfor <strong>eller</strong> tryk på søgeknappen for at fritekstsøge.</div>`;

    // Suggestions
    const suggestions = data.map(function (item) {
        return `
                <div class="search-suggestion-item" data-id="${item.id}" data-text="">
                    <div>
                        <a href="/${item.domain}/${item.id}">${item.display}</a>
                    </div>
                    <div>${item.sub_display}</div>
                </div>`;
    }).join('');

    return `${suggestionHelp} ${suggestions}`;
};

// Function to run when a suggestion is selected (On return)
const returnFunction = (data) => {
    const autocompleteElem = document.querySelector('.typeahead');

    let id = data.dataset.id
    // Set the value of the input field
    let selectedItem = currentAutoCompleteData.find(item => item.id == id)

    const displayValue = selectedItem.display;
    autocompleteElem.value = displayValue;

    // Get object id elem from form and set value
    const objectIdElem = document.querySelector('input[name="object_id"]');
    objectIdElem.value = id;

    // Get object domain elem from form and set value
    const objectDomainElem = document.querySelector('input[name="object_domain"]');
    objectDomainElem.value = selectedItem.domain;
}

function autoCompleteInit() {
    const autocompleteElem = document.querySelector('.typeahead');
    const suggestionsElem = document.querySelector('.search-suggestions');

    const options = {
        'autocompleteElem': autocompleteElem,
        'suggestionsElem': suggestionsElem,
        'renderFunction': renderFunction,
        'endpoint': `/auto_complete?q=`,
        'minInputLength': 2,
        'suggestionFocusClass': 'search-suggestion-focus',
        'returnFunction': returnFunction,
        'debug': false,
    }

    new AutoComplete(options);
}

const renderForm = function () {

    let relStart = '';
    let relEnd = '';
    if (resourceOriginal.domain === 'events' && resourceOriginal.date_from) {
        relStart = html`<input type="hidden" name="rel_start" value="${resourceOriginal.date_from}">`;
    }

    if (resourceOriginal.domain === 'events' && resourceOriginal.date_to) {
        relEnd = html`<input type="hidden" name="rel_end" value="${resourceOriginal.date_to}">`;
    }

    return html`
      <form id="relation-form" @submit=${submitRelationForm}>
        <input type="hidden" name="subject_domain" value="${resourceOriginal.domain}">
        <input type="hidden" name="subject_id" value="${resourceOriginal.id}">
        <input type="hidden" name="object_domain">
        <input type="hidden" name="object_id">
        ${relStart}
        ${relEnd}
        <label for="rel_label" class="float_left">Relationslabel</label>
        <input type="text" name="rel_label" class="float_left">
        <label for="object_label" class="float_left">Relationsobjekt</label>
        <input class="typeahead" name="object_label" type="text" autocomplete="off" placeholder="Find entitet">
        <button type="submit">Opret relation</button>
        <div class="search-suggestions"></div>
    `;
}

// Render a single section of the relations array
const renderRelationSection = (section, index) => html`
      <div class="record-section relations-edit">
        <div class="record-main">
          <h3 class="record-header">${section.label}<span class="relations-toggle" data-id="${index}" @click=${showRelationForm}> + </span> </h3>
            ${state.formShow == index ? renderForm() : ''}
            ${section.data.map(item => html`
                <div class="record-content">
                <div class="label">
                    <span class="relations-delete" @click=${deleteRelation} data-rel-id="${item.rel_id}" title="Fjern relation">x</span>
                    ${item.rel_label}
                </div>
                <div class="content">
                    <p>
                    <a href="/people/${item.id}">${item.display_label}</a>
                    </p>
                </div>
                </div>
            `)}
        </div>
      </div>
    `;

const deleteRelation = {
    async handleEvent(e) {
        let relId = e.target.dataset.relId;
        let url = `/relations/${relId}`;

        try {
            await Requests.asyncGetJson(url, 'DELETE');
            Flash.setMessage('Relationen er slettet', 'success');
            relations = await fetchRelations();
            renderRelationsMain();
        } catch (error) {
            Flash.setMessage('Kunne ikke slette relation', 'error');
            console.error(error);
        }
    }
}

const showRelationForm = {
    handleEvent(e) {
        let id = e.target.dataset.id;
        state.formShow = id
        renderRelationsMain();
        autoCompleteInit();

        let relationForm = document.getElementById('relation-form');
        relationForm.addEventListener('submit', function (e) {
            e.preventDefault();
        })
    }
}

const toogleEditMode = {
    handleEvent(e) {
        
        e.preventDefault();
        state.editEnabled = !state.editEnabled;

        // toggle relations
        const relationsElems = document.querySelectorAll('.relations');
        relationsElems.forEach((elem) => {
            elem.classList.toggle('hidden');
        });

        renderRelationsMain();

        // If state.editEnabled is true, then go to the first 'relations-edit' section
        // Else go to the first 'relations' section
        const firstSection = state.editEnabled ? document.querySelector('.relations-edit') : document.querySelector('.relations');
        firstSection.scrollIntoView({block: "start", inline: "nearest"});

        // If edit mode is turned off, then reload the current page
        if (!state.editEnabled) {
            location.reload();
        }
    }
}


const submitRelationForm = {
    async handleEvent(e) {
        e.preventDefault();
        let form = e.target;
        let data = new FormData(form);
        let url = '/relations';

        try {
            const result = await Requests.asyncPost(url, data)
            if (result.error) {
                console.log(result)
                throw new Error(result.message);
            }

            state.formShow = null;
            Flash.setMessage('Relationen er oprettet', 'success');
            relations = await fetchRelations();
            renderRelationsMain();
        } catch (error) {
            Flash.setMessage("Relationen kunne ikke oprettes. Der skal være en label og et objekt", 'error');
        }
    }
}

async function fetchRelations() {
    let url = `/relations/${resourceOriginal.domain}/${resourceOriginal.id}`;

    try {
        let result = await Requests.asyncGetJson(url);
        return result
    } catch (error) {
        Flash.setMessage('Kunne ikke opdatere relationer', 'error');
    }
}

// Iterate over the relations and render each section    
const renderRelationSections = function() {

    if (state.editEnabled) {
        return html`
        ${relations.map((section, index) => renderRelationSection(section, index))}
        ${editLink()}`;
    } else {
        return html`
        ${editLink()}`;

    }

}

function editLink () {

    let editLink;
    if (!state.editEnabled) {
        editLink = html`<a class="toogle-edit" href="#" @click=${toogleEditMode}>Rediger relationer</a>`;
    } else  {
        editLink = html`<a class="toogle-edit" href="#" @click=${toogleEditMode}>Afslut Redigering af relationer</a>`;
    }

    return html`<div class="sub-menu">${editLink}</div>`;
}

// Render the app
function renderRelationsMain() {
    const appElem = document.querySelector('.app');
    if (!appElem) return;
    render(renderRelationSections(), document.querySelector('.app'));
}

function initRelationsEdit(relationsInit, resourcesInit) {
    relations = relationsInit;
    resourceOriginal = resourcesInit;
    renderRelationsMain();
}

export { initRelationsEdit}
