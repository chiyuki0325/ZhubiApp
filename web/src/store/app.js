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

export const useWebSocketStore = defineStore('websocket', {
  state: () => ({
    sequence: 0,
    heartBeatLostCount: 0,
  }),
  getters: {
    getSequence: (state) => state.sequence,
    getHeartBeatLostCount: (state) => state.heartBeatLostCount,
  },
  actions: {
    increaseSequence() {
      this.sequence++
    },
    increaseHeartBeatLostCount() {
      this.heartBeatLostCount++
    }
  }
})
