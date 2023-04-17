// Adiciona o bootstrap e o fontawesome
import './sass/app.scss'
import * as bootstrap from 'bootstrap';
window.bootstrap = bootstrap;


/* import the fontawesome core */
import { library } from '@fortawesome/fontawesome-svg-core'

/* import font awesome icon component */
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

/* import specific icons */
import { fas } from '@fortawesome/free-solid-svg-icons';
import { fab } from "@fortawesome/free-brands-svg-icons";
import { far } from "@fortawesome/free-regular-svg-icons";

/* add icons to the library */
library.add(fas, fab, far)


// Cria a aplicação
import { createApp } from 'vue'
import App from './App.vue'
const app = createApp(App)

// Adiciona o pinia
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

// Adiciona o router
import router from './router'
app.use(router)

// Adiciona o vue-i18n
import i18n from './i18n'
app.use(i18n)

app.component('font-awesome-icon', FontAwesomeIcon)

// Adiciona o componente de layout
import AppLayout from './layouts/AppLayout.vue'
app.component('app-layout', AppLayout)

app.mount('#app')

