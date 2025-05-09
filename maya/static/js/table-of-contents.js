class TableOfContents {
    constructor(rootElement, autoGenerateIDs = false) {
        if (!rootElement || !(rootElement instanceof HTMLElement)) {
            throw new Error("Invalid root element provided");
        }

        this.rootElement = rootElement;
        this.toc = document.createElement('ul');
        this.currentUL = this.toc;
        this.autoGenerateIDs = autoGenerateIDs;
    }

    generateTOC() {
        if (this.autoGenerateIDs) {
            this._generateIDsForHeaders();
        }
        this._generateTOCFromHeaders();
        return this.toc;
    }

    _generateTOCFromHeaders() {
        const headers = Array.from(this.rootElement.querySelectorAll('h1, h2, h3, h4, h5, h6'));
        let previousLevel = 0;

        headers.forEach(header => {
            const headerLevel = parseInt(header.tagName.substring(1), 10);

            if (headerLevel > previousLevel) {
                const newUL = document.createElement('ul');
                this.currentUL.appendChild(newUL);
                this.currentUL = newUL;
            } else if (headerLevel < previousLevel) {
                let levelDiff = previousLevel - headerLevel;
                while (levelDiff > 0) {
                    this.currentUL = this.currentUL.parentNode;
                    levelDiff--;
                }
            }

            const newLI = this._createListItem(header);
            this.currentUL.appendChild(newLI);
            previousLevel = headerLevel;
        });
    }

    _isHeader(element) {
        return /^H[1-6]$/.test(element.tagName);
    }

    _createListItem(element) {
        const item = document.createElement('li');
        const link = document.createElement('a');
        link.href = '#' + element.id;
        link.textContent = element.textContent;
        item.appendChild(link);
        return item;
    }

    _generateIDsForHeaders() {
        let idCount = 0;
        Array.from(this.rootElement.querySelectorAll('h1, h2, h3, h4, h5, h6')).forEach(header => {
            if (!header.id) {
                header.id = `header-${idCount++}`;
            }
        });
    }
}

/**
 * Show the table of content based on the sourceElement and tocElement
 * sourceElement is the element that contains the content
 * tocElement is the element that the TOC will be appended to
 * 
 * By default only h1, h2, h3, h4, h5, h6 will be included in the TOC
 * These need to have an id attribute to be included in the TOC
 * 
 * autoGenerateIDs is a flag to automatically generate ids for headers, 
 * so that they can be included in the TOC
 * 
 * @param {*} sourceElement 
 * @param {*} tocElement 
 * @param {*} autoGenerateIDs 
 */
function showTOC(sourceElement, tocElement, autoGenerateIDs = false) {
    const tocGenerator = new TableOfContents(sourceElement, autoGenerateIDs);
    const toc = tocGenerator.generateTOC();
    tocElement.appendChild(toc); 
}

export { showTOC };
