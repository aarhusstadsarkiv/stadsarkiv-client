/**
 * 
 * @param {*} id 
 * @param {*} value 
 * @param {int} ttl time to live in seconds 
 */
function setLocalStorage(id, value, ttl) {
    if (typeof(Storage) !== "undefined") {
        var now = new Date();
        var item = {
            value: value,
            expiry: now.getTime() + (ttl * 1000)
        }

        localStorage.setItem(id, JSON.stringify(item));
    }
}

function getLocalStorage(id) {
    if (typeof(Storage) !== "undefined") {
        var itemStr = localStorage.getItem(id);
        if (!itemStr) {
            return null;
        }
        var item = JSON.parse(itemStr);
        var now = new Date();
        if (now.getTime() > item.expiry) {
            localStorage.removeItem(id);
            return null;
        }
        return item.value;
    }
    return null;
}

function removeLocalStorage(id) {
    if (typeof(Storage) !== "undefined") {
        localStorage.removeItem(id);
    }
}

export { setLocalStorage, getLocalStorage, removeLocalStorage}
