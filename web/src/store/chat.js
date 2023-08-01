// Utilities
import {defineStore} from 'pinia'
import {api, useAuth, prettifyName} from '@/utils'


export const useChatStore = defineStore('chat', {
  state: () => ({
    chats: [],
  }),
  actions: {
    setChats(chats) {
      this.chats = chats
    },
    sortByDate() {
      this.chats.sort((a, b) => {
        return new Date(b.last_updated) - new Date(a.last_updated)
      })
    },
    async touchChat(message) {
      // 更新修改时间
      const {chat_id, last_updated, id} = message
      const chat = this.chats.find(chat => chat.id === chat_id)
      if (chat) {
        chat.last_updated = last_updated
        chat.last_message_db_id = id
        // TODO: 在此处就渲染消息
        // TODO: 用户
        chat.last_message = message.text || message.caption || message.sticker?.emoji || message.system_message || '[消息]'
        const userStore = useUserStore()
        userStore.tryFetchUser(message.sender_id).then(() => {
          const user = userStore.getUser(message.sender_id)
          chat.last_message_sender = prettifyName(user)
          this.sortByDate()
        })
      }
    },
  }
})
export const useMessageStore = defineStore('message', {
  state: () => ({
    messages: []
  }),
  actions: {
    addMessage(message) {
      this.messages.push(message)
    },
    async tryFetchMessageByDbId(db_id) {
      if (!db_id) return
      if (this.messages.find(message => message.id === db_id)) return
      await api.get(
        `/tg/message/by_db_id/${db_id}`,
        useAuth()
      ).then(res => {
        if (res.status !== 200) {
          console.error(res)
        } else {
          this.addMessage(res.data.message)
        }
      })
    }
  },
  getters: {
    getMessageByDbId: (state) => {
      return (db_id) => state.messages.find(message => message.id === db_id)
    }
  }
})

export const useUserStore = defineStore('user', {
  state: () => ({
    users: []
  }),
  actions: {
    addUser(user) {
      this.users.push(user)
    },
    async tryFetchUser(user_id) {
      if (!user_id) return
      if (this.users.find(user => user.id === user_id)) return
      await api.get(
        `/tg/user/${user_id}/info`,
        useAuth()
      ).then(res => {
        if (res.status !== 200) {
          console.error(res)
        } else {
          this.addUser(res.data.user)
        }
      })
    }
  },
  getters: {
    getUser: (state) => {
      return (user_id) => state.users.find(user => user.id === user_id)
    }
  }
})
