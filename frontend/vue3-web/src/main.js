import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import { createPersistedState } from 'pinia-plugin-persistedstate'

const app = createApp(App)

app.use(createPinia({
  state: createPersistedState({
    storage: localStorage,
  })
}))
app.use(router)
app.use(ElementPlus)

app.mount('#app')
