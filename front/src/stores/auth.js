import { defineStore } from 'pinia';
import moment from "moment";
import axios from 'axios';
// import api from '../api';


export const authStore = defineStore('auth', {
    state: () => ({
        // Token
        access_token: '',
        token_type: '',
        expire: '',
        // User
        id: null,
        username: '',
        email: '',
        name: '',
        is_superuser: false,
        groups: [],
        permissions: [],
    }),
    getters: {
        auth(state) {
            return state.id != null && state.access_token.length > 0;
        },
        perms: (state) => (perm) => {
            if (state.auth) {
                if (state.is_superuser) return true;
                if (Array.isArray(perm) && perm.length > 0) {
                    for (let key in perm) if (state.permissions.includes(perm[key])) return true;
                } else return perm.length == 0 ? true : state.permissions.includes(perm);
            }
            return false;
        },
        token(state) {
            if (state.expire.length == 0) return '';
            return state.token_type + " " + state.access_token;
        },
        is_expired(state) {
            if (state.expire.length == 0) return true;
            return moment(state.expire).diff(moment(), 'seconds') < 80;
        },
    },
    actions: {
        async login(username, password) {
            let lang = localStorage.getItem('lang') || import.meta.env.VITE_I18N_LOCALE || 'en';
            let res = await axios.post('/auth/token', {
                username: username,
                password: password
            }, {
                baseURL: import.meta.env.VITE_API,
                headers: {
                    "Accept-Language": lang.replace("_", "-")
                },
            });
            this.loadData(res.data);
        },
        async refresh() {
            let lang = localStorage.getItem('lang') || import.meta.env.VITE_I18N_LOCALE || 'en';
            let res = await axios.get('/auth/refresh', {
                baseURL: import.meta.env.VITE_API,
                headers: {
                    "Accept-Language": lang.replace("_", "-"),
                    "Authorization": this.token
                },
            });
            this.loadData(res.data);
        },
        loadData({
            access_token = '',
            token_type = '',
            expire = "",
            user = {}
        }) {
            this.access_token = access_token;
            this.token_type = token_type;
            this.expire = expire;
            Object.assign(this, user);
        },
        logout() {
            this.$reset();
        }
    },
    persist: true,
});