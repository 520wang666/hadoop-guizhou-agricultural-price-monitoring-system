import { createPinia } from 'pinia'
import { createPersistedState } from 'pinia-plugin-persistedstate'
import { useUserStore } from './modules/user'
import { usePriceStore } from './modules/price'

export const store = createPinia({
  state: createPersistedState({
    storage: localStorage,
  }),
  modules: {
    user: useUserStore,
    price: usePriceStore
  }
})

export default store
