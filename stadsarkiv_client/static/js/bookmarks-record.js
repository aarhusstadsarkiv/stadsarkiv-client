
import { asyncLogError } from "/static/js/error.js";
import { Requests } from "/static/js/requests.js";
import { Flash } from "/static/js/flash.js";

let action;
const bookmarkAddElem = document.getElementById('bookmark-action');
const recordId = parseInt(bookmarkAddElem.getAttribute('data-id'));

const initialize = async () => {
    let bookmarks_json = await Requests.asyncGetJson('/auth/bookmarks_json', 'GET');

    function bookmark_isset(bookmarks, recordId) {
        return bookmarks.some(bookmark => bookmark.record_id === recordId);
    }

    if (bookmark_isset(bookmarks_json, recordId)) {
        bookmarkAddElem.innerHTML = 'Fjern bogmærke';
        action = 'remove';
        bookmarkAddElem.setAttribute('data-action', action);
    } else {
        bookmarkAddElem.innerHTML = 'Tilføj bogmærke';
        action = 'add';
        bookmarkAddElem.setAttribute('data-action', action);
    }
}

await initialize();

const get_data = () => {
    const data = { record_id: recordId, action: action };
    return JSON.stringify(data);
}

const spinner = document.querySelector('.loadingspinner');
bookmarkAddElem.addEventListener('click', async function (e) {
    let res;
    e.preventDefault();
    spinner.classList.toggle('hidden');
    try {
        const data = get_data();
        res = await Requests.asyncPostJson('/auth/bookmarks', data, 'POST');
        if (res.error) {
            Flash.setMessage(res.message, 'error');
        } else {
            Flash.setMessage(res.message, 'success');
        }
    } catch (e) {
        Flash.setMessage(res.message, 'error');
        await asyncLogError('/error/log', e.stack);
    } finally {
        initialize();
        spinner.classList.toggle('hidden');
    }
});
