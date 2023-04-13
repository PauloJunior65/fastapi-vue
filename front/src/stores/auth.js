import { defineStore } from 'pinia'
// import api from '../api'

export const authStore = defineStore('auth', {
    state: () => ({
        access: "",
        refresh: "",
        id: null,
        username: '',
        password: '',
        email: '',
        name: '',
        is_superuser: false,
        date_joined: '',
        created_at: '',
        updated_at: '',
        groups: [],
        permissions: [],
        expire: '',
    }),
    getters: {
        auth(state) {
            return state.id != null && state.access.length > 0 && state.refresh.length > 0;
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
            return "Token " + state.access;
        }
    },
    actions: {

    },
    persist: true,
});