import axios from "axios";
import { authStore } from './stores/auth';
const store = authStore();

function api({ auth = true, download = false } = {}) {
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