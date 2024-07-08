// Used on the list of bookmarks for the user
import { Requests } from "/static/js/requests.js";
import { Flash } from "/static/js/flash.js";
import { asyncLogError } from "/static/js/error.js";

const spinner = document.querySelector('.loadingspinner');
const bookmarkElems = document.querySelectorAll('.bookmark-delete');

bookmarkElems.forEach((elem) => {

    const recordId = elem.getAttribute('data-id');
    const get_data = () => {
        const data = { record_id: recordId, action: 'remove' };
        return JSON.stringify(data);
    }

    elem.addEventListener('click', async (e) => {
        let res;
        spinner.classList.remove('hidden');
        try {
            e.preventDefault();
            const data = get_data();
            res = await Requests.asyncPostJson('/auth/bookmarks', data, 'POST');
            if (res.error) {
                Flash.setMessage(res.message, 'error');
            } else {
                elem.closest('.record-section').remove();
                Flash.setMessage(res.message, 'success');
            }
        } catch (error) {
            Flash.setMessage(res.message, 'error');
            await asyncLogError('/error/log', e.stack);
        } finally {
            spinner.classList.add('hidden');
        }
    });
})