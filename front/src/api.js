import axios from "axios";
import { exceptions, error_mensage, error_fields } from "./exceptions";
import { authStore } from './stores/auth';

/**
 * API instance
 * @param {Object} params - Params object
 * @param {Boolean} params.auth - If true, add Authorization header
 * @param {Boolean} params.download - If true, set responseType to blob
 * @param {String} params.content_type - Set content-type
 * @returns {AxiosInstance}
 */
function api({ auth = true, download = false, content_type = null } = {}) {
    let store = authStore();
    let lang = localStorage.getItem('lang') || import.meta.env.VITE_I18N_LOCALE || 'en';
    let base = window.location.origin.split(':');
    if (base.length > 2) base.length = 2;
    let url = import.meta.env.VITE_API || `${base.join(':')}:8001/`
    if (!isNaN(parseInt(url))) url = `${base.join(':')}:${parseInt(import.meta.env.VITE_API)}/`;
    let config = {
        baseURL: url,
        headers: {
            "Accept-Language": lang.replace("_", "-"),
        },
    };
    if (auth && store.auth) config.headers["Authorization"] = store.token;
    if (content_type != null) config.headers["content-type"] = content_type;
    if (download) config["responseType"] = 'blob';
    return axios.create(config);
}

export default api;
export { api, exceptions, error_mensage, error_fields };