/* Setting up Router For the project */
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

// Mounting the app to the DOM
createApp(App)
    .use(router)
    .mount('#app')