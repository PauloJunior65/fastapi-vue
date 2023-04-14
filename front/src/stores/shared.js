import { defineStore } from 'pinia';


export const sharedStore = defineStore('shared', {
    state: () => ({
        $router: null,
    }),
    getters: {

    },
    actions: {
        error(code = 400, message = '') {
            if (this.$router == null) return;
            this.$router.replace({ name: 'error', state: { code: code, message: message } });
        }
    },
});