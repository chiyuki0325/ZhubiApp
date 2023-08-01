// Utilities
import {defineStore} from 'pinia'


export const useSettingStore = defineStore('settings', {
  state: () => ({
    rail: true,
    chatListRail: false,
    tab: 'all'
  })
})
