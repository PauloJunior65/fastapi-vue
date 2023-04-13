<template>
    <select class="form-select" v-model="lang">
        <option v-for="locale in $i18n.availableLocales" :key="`locale-${locale}`" :value="locale">
            {{ locale.toUpperCase().replace(/_/g, "-") }}
        </option>
    </select>
</template>
<script>
import { defineComponent } from "vue";

export default defineComponent({
    mounted() {
        document.documentElement.setAttribute("lang", this.$i18n.locale.replace("_", "-"));
    },
    computed: {
        lang: {
            get() {
                return this.$i18n.locale;
            },
            set(value) {
                this.$i18n.locale = value;
                localStorage.setItem('lang', value);
            },
        }
    },
    methods: {
        logout() {

        },
    },
});
</script>