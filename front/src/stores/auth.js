import { defineStore } from 'pinia';
import moment from "moment";
import api from '@/api';
import { sharedStore } from './shared';


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
            if (state.expire.length > 0 && moment(state.expire).diff(moment(), 'seconds') <= 0) {
                this.$reset();
                return false;
            }
            return state.id != null && state.access_token.length > 0;
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
        perms(perm) {
            if (this.auth) {
                if (this.is_superuser) return true;
                if (Array.isArray(perm) && perm.length > 0) {
                    for (let key in perm) if (this.permissions.includes(perm[key])) return true;
                } else return perm.length == 0 ? true : this.permissions.includes(perm);
            }
            return false;
        },
        async login(username, password) {
            console.log(username, password);
            let res = await api({ auth: false, content_type: 'application/x-www-form-urlencoded' }).post('/token', {
                username: username,
                password: password
            });
            this.loadData(res.data);
        },
        async refresh() {
            let lang = localStorage.getItem('lang') || import.meta.env.VITE_I18N_LOCALE || 'en';
            let res = await api().get('/refresh', {
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
            const store = sharedStore();
            store.replace('login');
        }
    },
    persist: true,
});