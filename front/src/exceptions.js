import { sharedStore } from './stores/shared';

function exceptions({ code = null, message = '', name = null, response = { status: null, statusText: '', data: {} }, request = { status: null }, codeIgnore = [] } = {}) {
    if (codeIgnore.includes(code) || codeIgnore.includes(response.status) || codeIgnore.includes(request.status)) return false;
    const store = sharedStore();
    if (response.data.detail != undefined) {
        store.error(response.status, response.data.detail);
    } else if (response.status != null) {
        store.error(response.status, response.statusText);
    } else if (code != null) {
        store.error(code, message);
    } else if (name != null) {
        store.error(name, message);
    }
    return true;
}
export default exceptions;