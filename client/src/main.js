import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import * as bootstrap from 'bootstrap'
import axios from 'axios'
import Cookies from 'js-cookie'

axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken')


window.bootstrap = bootstrap

createApp(App).use(router).mount('#app')