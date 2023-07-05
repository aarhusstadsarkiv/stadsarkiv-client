// Function to save the state of the tree to local storage
function saveTree() {
    const detailsElements = document.querySelectorAll('details');
    const state = [];

    detailsElements.forEach((detailsElement) => {
        const isOpen = detailsElement.hasAttribute('open');
        state.push(isOpen);
    });

    localStorage.setItem('treeState', JSON.stringify(state));
}

// Function to expand the tree based on the saved state from local storage
function expandTree() {
    const savedState = localStorage.getItem('treeState');

    if (savedState) {
        const state = JSON.parse(savedState);
        const detailsElements = document.querySelectorAll('details');

        detailsElements.forEach((detailsElement, index) => {
            const isOpen = state[index];
            if (isOpen) {
                detailsElement.setAttribute('open', 'true');
            } else {
                detailsElement.removeAttribute('open');
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    try {
        expandTree();
        window.addEventListener('beforeunload', saveTree);
    
    } catch (error) {
        // unset local storage if it fails. The tree may be updated and the saved state may be invalid
        localStorage.removeItem('treeState');
        console.log(error);
    }
});
