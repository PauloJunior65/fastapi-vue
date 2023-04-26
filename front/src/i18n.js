import { createI18n } from 'vue-i18n'

import en from './locales/en.json'
import pt from './locales/pt.json'

const instance = createI18n({
    // silentTranslationWarn: true,
    // silentFallbackWarn: true,
    locale: localStorage.getItem('lang') || import.meta.env.VITE_I18N_LOCALE || 'en',
    fallbackLocale: import.meta.env.VITE_I18N_FALLBACK_LOCALE || 'en',
    messages: {
        en,
        pt
    }
});

export default instance;

export const i18n = instance.global;