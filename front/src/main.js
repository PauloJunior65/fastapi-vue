// Adiciona o bootstrap e o fontawesome
import './bootstrap'

// Cria a aplicação
import { createApp } from 'vue'
import App from './App.vue'
const app = createApp(App)

// Adiciona o pinia
import { createPinia } from 'pinia'
app.use(createPinia())

// Adiciona o router
import router from './router'
app.use(router)

// Adiciona o vue-i18n
import i18n from './i18n'
app.use(i18n)

// Adiciona o componente de ícones do fontawesome
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
app.component('font-awesome-icon', FontAwesomeIcon)
app.config.productionTip = false

// Adiciona o componente de layout
import AppLayout from './layouts/AppLayout.vue'
app.component('app-layout', AppLayout)

app.mount('#app')

