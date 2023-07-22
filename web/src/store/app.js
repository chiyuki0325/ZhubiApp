// Utilities
import {defineStore} from 'pinia'


export const useSettingStore = defineStore('settings', {
  state: () => ({
    rail: true,
    tab: 'allChats'
  })
})

export const useChatStore = defineStore('chat', {
  state: () => ({
    chats: [],
  })
})
export const useMessageStore = defineStore('message', {
  state: () => ({
    messages: [],
  })
})
