import { asyncLogError } from "/static/js/error.js";
import { Requests } from "/static/js/requests.js";
import { Flash } from "/static/js/flash.js";

const spinner = document.querySelector('.loadingspinner');
const orderElem = document.getElementById('record-order');

// <div class ="action-links"><a href="#" id="record-order" data-id="1">Bestil materialet</a></div>
console.log(orderElem)

if (orderElem) {
    orderElem.addEventListener('click', async function (event) {
        event.preventDefault();
        Flash.clearMessages();
        spinner.classList.toggle('hidden');
        try {

            const recordId = orderElem.getAttribute('data-id');
            const url = `/order/${recordId}`;            
            const res = await Requests.asyncPostJson(url, {});
            if (res.error) {
                console.log(res.message);
                Flash.setMessage(res.message, 'error');
            } else {
                Flash.setMessage(res.message, 'success');
                orderElem.innerText = 'Materialet er bestilt';
                orderElem.setAttribute('disabled', 'true'); 
            }

        } catch (e) {
            Flash.setMessage(res.message, 'error');
            await asyncLogError('/error/log', e.stack);
        } finally {
            spinner.classList.toggle('hidden');
        }
    });
}