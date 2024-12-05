import { asyncLogError } from "/static/js/error.js";
import { Requests } from "/static/js/requests.js";
import { Flash } from "/static/js/flash.js";

const spinner = document.querySelector('.loadingspinner');
const deleteElements = document.querySelectorAll('.delete-order > *');

deleteElements.forEach(element => {
    element.addEventListener('click', async function (event) {

        const res = confirm('Er du sikker på at du vil slette denne bestilling?');
        if (!res) {
            return;
        }

        event.preventDefault();
        Flash.clearMessages();
        spinner.classList.toggle('hidden');

        const formData = new FormData();
        formData.append('finished', 1);

        try {
            const recordSection = element.closest('.record-section');
            const url = '/order/patch/' + element.dataset.id;
            const res = await Requests.asyncPost(url, formData);

            if (res.error) {
                Flash.setMessage(res.message, 'error');
            } else {
                Flash.setMessage(res.message, 'success');
                recordSection.remove();
            }

        } catch (e) {
            Flash.setMessage(res.message, 'error');
            await asyncLogError('/error/log', e.stack);
        } finally {
            spinner.classList.toggle('hidden');
        }
    });
});

export { }; 
