// Utilities
import {defineStore} from 'pinia'


export const useChatStore = defineStore('chat', {
  state: () => ({
    chats: {},
  })
})
export const useMessageStore = defineStore('message', {
  state: () => ({
    messages: [],
  })
})

export const useUserStore = defineStore('chat', {
  state: () => ({
    users: {},
  }),
  actions: {
    addUser(user) {
      this.users[user.id] = user
    }
  },
  getters: {
    getUser: (state) => {
      return (id) => {
        return state.users[id]
      }
    }
  }
})
