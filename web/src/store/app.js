// Utilities
import {defineStore} from 'pinia'
import {useLocalStorage} from '@vueuse/core'

export const useSettingStore = defineStore('settings', {
  state: () => ({
    rail: true,
    chatListRail: false,
    tab: 'all',
  })
})

export const useThemeStore = defineStore('theme', {
  state: () => ({
    theme: useLocalStorage('theme', 'BlueMountainsLight', {mergeDefaults: true}),
  }),
})
