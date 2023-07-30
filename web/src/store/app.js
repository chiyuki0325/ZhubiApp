// Utilities
import {defineStore} from 'pinia'


export const useSettingStore = defineStore('settings', {
  state: () => ({
    rail: true,
    tab: 'all'
  })
})
