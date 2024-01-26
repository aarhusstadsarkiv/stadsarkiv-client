class TableOfContents {
    constructor(rootElementId) {
        this.rootElement = document.getElementById(rootElementId);
        this.toc = document.createElement('ul');
        this.currentUL = this.toc;
        this.firstHeaderFound = false; // Flag to track if the first header is found
    }

    generateTOC() {
        this._generateTOCForElement(this.rootElement, 0);
        return this.toc;
    }

    _generateTOCForElement(element, level) {
        Array.from(element.children).forEach(child => {
            if (this._isHeader(child) && child.id) {
                const headerLevel = parseInt(child.tagName.substring(1), 10);

                if (!this.firstHeaderFound) {
                    level = headerLevel; // Start the TOC at the level of the first header
                    this.firstHeaderFound = true;
                }

                while (headerLevel > level) {
                    const newUL = document.createElement('ul');
                    if (this.currentUL.lastElementChild) {
                        this.currentUL.lastElementChild.appendChild(newUL);
                    } else {
                        this.currentUL.appendChild(newUL);
                    }
                    this.currentUL = newUL;
                    level++;
                }

                while (headerLevel < level) {
                    this.currentUL = this.currentUL.parentNode.parentNode;
                    level--;
                }

                const newLI = this._createListItem(child);
                this.currentUL.appendChild(newLI);
                this._generateTOCForElement(child, level);
            } else {
                this._generateTOCForElement(child, level);
            }
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
}

/**
 * Show the table of content based on the sourceID and tocID
 * sourceID: the id of the source, e.g. <div id="article">...</div>
 * tocID: the id of the table of content, e.g. <div id="toc">...</div>
 * @param {*} sourceID 
 * @param {*} tocID 
 */
function showTOC(sourceID, tocID) {
    const tocGenerator = new TableOfContents(sourceID);
    const toc = tocGenerator.generateTOC();
    document.getElementById(tocID).appendChild(toc);
}

export { showTOC };