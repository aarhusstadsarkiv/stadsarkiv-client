/**
 * Get a Path segment of the window.location.pathname
 */
function getPathPart(num, path) {
    if (!path) {
        path = window.location.pathname;
    }
    var ary = path.split('/');
    ary.shift();
    return ary[num];
}

export {getPathPart}