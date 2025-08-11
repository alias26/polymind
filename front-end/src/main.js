import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { pinia } from './store'

// FontAwesome CSS import
import '@fortawesome/fontawesome-free/css/all.css'

// 공통 스타일 import
import './assets/buttons.css'
import './assets/z-index.css'

createApp(App).use(pinia).use(router).mount('#app')
