import axios from "axios";
import { exceptions, error_mensage, error_fields } from "./exceptions";
import { authStore } from './stores/auth';

/**
 * API instance
 * @param {Object} params - Params object
 * @param {Boolean} params.auth - If true, add Authorization header
 * @param {Boolean} params.download - If true, set responseType to blob
 * @returns {AxiosInstance}
 */
function api({ auth = true, download = false } = {}) {
    const store = authStore();
    let lang = localStorage.getItem('lang') || import.meta.env.VITE_I18N_LOCALE || 'en';
    let config = {
        baseURL: import.meta.env.VITE_API,
        headers: {
            "Accept-Language": lang.replace("_", "-"),
        },
    };
    if (auth && store.auth) config.headers["Authorization"] = store.token;
    if (download) config["responseType"] = 'blob';
    return axios.create(config);
}

export default api;
export { api, exceptions, error_mensage, error_fields };