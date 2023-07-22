// Utilities
import {createPinia} from 'pinia'

export const store = createPinia()

export default {
  install: (app) => {
    app.use(store)
  }
}
