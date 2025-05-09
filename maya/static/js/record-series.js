
let oneDay = 60 * 60 * 24;
const writeToCache = function (url, data) {
    const expiration = Date.now() + oneDay * 1000;
    const cacheData = { data, expiration };
    localStorage.setItem(url, JSON.stringify(cacheData));
};

const readFromCache = function (url) {
    const cacheData = JSON.parse(localStorage.getItem(url));

    if (cacheData && cacheData.expiration >= Date.now()) {
        return cacheData.data;
    } else {
        localStorage.removeItem(url);
        return null;
    }
};

async function loadSeries() {

    let json = readFromCache(collectionJsonPath);
    if (json) return json

    let data = await fetch(collectionJsonPath)
        .then(response => response.json())
        .then(data => {
            return data;
        });

    if (data.series) {
        writeToCache(collectionJsonPath, data.series);
    } else {
        throw new Error('No series found');
    }
    return data.series
}

function decodeSerieUrl(url) {
    var decodedUrl = decodeURIComponent(url.replace(/\+/g, ' '));
    return decodedUrl
}

/**
 * ID counter
 */
let id = 1;

/**
 * Add 'id', 'newLink', 'init', and 'active' to each item in series
 * 
 * 'id' is used to find the item in the tree
 * 'newLink' is used to create the link in the tree
 * 'init' is used is shown on page load
 * 'active' indicates if the item is active
 * 
 */

function addDataToSeries(children) {
    for (let i = 0; i < children.length; i++) {
        let child = children[i];
        child.id = id++;

        let newLinkCompare = `collection=${collectionId}&series=${child.path}`;
        let newLink = `/search?collection=${collectionId}&series=${encodeURIComponent(child.path)}`;
        child.newLink = newLink;

        for (let j = 0; j < seriesInit.length; j++) {
            const seriesInitItem = seriesInit[j];
            if (decodeSerieUrl(seriesInitItem.new_link) === newLinkCompare) {
                child.active = true;
                child.init = true;
                child.expanded = false;
                seriesInitItem.id = child.id;
                break;
            } else {
                child.active = false;
                child.expanded = false;
                child.init = false;
            }
        }

        if (child.children) {
            addDataToSeries(child.children);
        }
    }
}

/**
 * Flag that checks if the first item is being created
 * No arrow if first item
 */
let first = true;

/**
 * Generate the HTML from the collectionData's state
 */
function collectionDataAsUL(collectionData) {

    let html = '<ul class="record">';
    for (let i = 0; i < collectionData.length; i++) {
        const item = collectionData[i];

        let initClass = '';
        if (item.init) initClass = 'init';
        if (!item.active && !item.init) continue;

        let span = `<i class="fas fa-arrow-right fa-sm"></i>`;
        if (first) {
            span = `<i class="first"></i>`;
            first = false;
        }

        let link = `<a class="serie-link ${initClass}" href="${item.newLink}">${span} ${item.label}</a>`;
        if (item.children) {
            let expandedClass = 'far fa-folder';
            if (item.expanded) expandedClass = 'expanded far fa-folder-open ';
            link += `<i data-id="${item.id}" class="serie-toogle ${expandedClass}"></i>`;
        }

        html += `<li class="record">${link}`;
        if (item.children) {
            html += collectionDataAsUL(item.children);
        }

        html += `</li>`
    }
    html += '</ul>';
    return html;
}

/**
 * Search for a node in the tree by id
 */
function findById(tree, nodeId) {
    for (let node of tree) {
        if (node.id === nodeId) return node

        if (node.children) {
            let desiredNode = findById(node.children, nodeId)
            if (desiredNode) return desiredNode
        }
    }
    return false
}

/**
 * Get the collection data by label
 */
function getCollectionDataByLabel(collectionData, label) {
    for (let i = 0; i < collectionData.length; i++) {
        const item = collectionData[i];
        if (item.label === label) return item
    }
    return false
}

/**
 * Load the series data and create the HTML
 */
const collectionDataArray = []
const seriesApp = document.querySelector('#series-app');
document.addEventListener('DOMContentLoaded', async function () {

    try {

        // Get first item in seriesInit
        let serie = seriesInit[0];
        let series = await loadSeries();

        addDataToSeries(series);

        // Get collection data
        let collectionData = getCollectionDataByLabel(series, serie.label);
        collectionDataArray.push(collectionData)

        let appHTML = collectionDataAsUL(collectionDataArray);
        seriesApp.innerHTML = appHTML;

    } catch (error) {
        console.log(error);
    }

});

document.addEventListener('click', async function (event) {

    try {

        if (event.target.matches('i.serie-toogle')) {

            event.preventDefault();
            let elem = event.target;
            let id = elem.dataset.id;
            let node = findById(collectionDataArray, parseInt(id));

            // Switch state
            node.expanded = !node.expanded;

            if (node.children) {
                node.children.forEach(function (child) {
                    if (node.expanded) {
                        child.active = true
                    } else {
                        child.active = false
                    }
                })

                first = true;
                let appHTML = collectionDataAsUL(collectionDataArray);
                seriesApp.innerHTML = appHTML;
            }
        }
    } catch (error) {
        console.log(error);
    }
}, false);
