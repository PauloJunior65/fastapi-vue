import { sharedStore } from './stores/shared';

/**
 * Redireciona para a página de erro
 * @param {Object} axios - Axios error object
 * @param {Array<Number>} axios.codeIgnore - Array of codes to ignore
 * @param {boolean} axios.valid - If true, 422 status code will be ignored
 * @returns {boolean} true if exception is handled
 */
function exceptions({ codeIgnore = [], valid = false, code = null, message = '', name = null, response = { status: null, statusText: '', data: {} }, request = { status: null } } = {}) {
    if (valid && response.status == 422) return false;
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

/**
 * Pegar a mensagem de erro
 * @param {Object} axios - Axios error object 
 * @returns {string} Error mensage 
 */
function error_mensage({ message = undefined, response = { statusText: undefined, data: {} } } = {}) {
    if (response.data != undefined) if (response.data.detail != undefined) return response.data.detail;
    if (Array.isArray(response.data)) for (const item of response.data) if (item.msg != undefined) return item.msg;
    if (response.statusText != undefined) return response.statusText;
    if (message != undefined) return message;
    return '';
}

/**
 * Pegar os campos de erro
 * @param {Object} axios - Axios error object 
 * @returns {Object} Error fields { field: { msg: string, type: string } }
 */
function error_fields({ response = { data: [] } } = {}) {
    if (response.data != undefined && Array.isArray(response.data)) return response.data.reduce((acc, item) => {
        if (item.msg != undefined && item.type != undefined && Array.isArray(item.loc) && item.loc.length > 0) acc[item.loc[item.loc.length > 1 ? 1 : 0]] = { msg: item.msg, type: item.type };
        return acc;
    }, {});
    return {};
}
export { exceptions, error_mensage, error_fields };