import axios from "axios";
import exceptions from "./exceptions";
import { authStore } from './stores/auth';


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
export { api, exceptions };