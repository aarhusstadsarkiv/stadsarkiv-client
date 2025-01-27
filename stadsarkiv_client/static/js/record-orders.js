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
        spinner.classList.toggle('hidden');
        let res;
        try {

            const recordId = orderElem.getAttribute('data-id');
            const action = orderElem.getAttribute('data-action');
            
            let url;
            let data;
            
            if (action === 'create') {

                url = `/order/${recordId}`;
                data = {}
            } else {
                url = `/order/delete/${recordId}`;
                data = {}

                const confirmedDelete = confirm('Er du sikker på at du vil slette bestillingen?');
                if (!confirmedDelete) {
                    return;
                }
            }

            res = await Requests.asyncPostJson(url, {});
            
            if (res.error) {
                console.log(res.message);
                Flash.setMessage(res.message, 'error');
            } else {

                if (action === 'delete') {
                    Flash.setMessage(res.message, 'success');
                    orderElem.innerText = 'Bestil til læsesal';
                    orderElem.setAttribute('data-action', 'create');
                }

                if (action === 'create') {
                    Flash.setMessage(res.message, 'success');
                    orderElem.innerText = 'Slet bestilling';
                    orderElem.setAttribute('data-action', 'delete');
                }
            }

        } catch (e) {
            Flash.setMessage(res.message, 'error');
            await asyncLogError('/error/log', e.stack);
        } finally {
            spinner.classList.toggle('hidden');
        }
    });
}
