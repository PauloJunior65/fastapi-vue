import { defineStore } from 'pinia'

export const authStore = defineStore('auth', {
    state: () => ({

    }),
    getters: {
        is_auth() {
            return false
        },
        perms() {
            return false
        },
    },
    actions: {

    },
    persist: true,
});