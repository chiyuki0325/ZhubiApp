// Utilities
import {defineStore} from 'pinia'

export const useApiUrlStore = defineStore('apiPath', {
  state: () => ({
    apiUrl: 'http://localhost:5586'
  }),
})
