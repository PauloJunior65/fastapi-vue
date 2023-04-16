import { defineStore } from 'pinia';


export const sharedStore = defineStore('shared-vue', {
    state: () => ({
        $router: null,
        translation: null,
        sizePerPage: 50,
    }),
    getters: {
        $t: (state) => (key) => {
            if (state.translation == null) return key;
            return state.translation(key);
        },
    },
    actions: {
        error(code = 400, message = '') {
            if (this.$router == null) return;
            this.$router.replace({ name: 'error', state: { code: code, message: message } });
        },
        replace(name, params = {}, query = {}) {
            if (this.$router == null) return;
            this.$router.replace({ name: name, params: params, query: query });
        },
        push(name, params = {}, query = {}) {
            if (this.$router == null) return;
            this.$router.push({ name: name, params: params, query: query });
        },
    },
});