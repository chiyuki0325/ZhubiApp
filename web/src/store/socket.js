import {defineStore} from "pinia"
import {operations} from "@/config/socket"
import Cookies from "js-cookie"

// 其它 store
import {useMessageStore, useChatStore} from "@/store/chat"


export const useWebSocketStore = defineStore('websocket', {
  state: () => ({
    socket: null,
    isConnected: false,
    message: '',
    reconnectError: false,
    heartBeatInterval: 30000, // 30s
    heartBeatTimer: 0
  }),
  actions: {
    SOCKET_ONOPEN(event) {
      const token = Cookies.get('token') || ''
      this.socket = event.currentTarget
      this.isConnected = true
      // 连接成功时启动定时发送心跳消息，避免被服务器断开连接
      this.isConnected && this.socket.sendObj({
        op: operations.ping,
        d: {},
        t: token
      })
      this.heartBeatTimer = setInterval(() => {
        this.isConnected && this.socket.sendObj({
          op: operations.heartbeat,
          d: {},
          t: token
        })
      }, this.heartBeatInterval)
    },
    SOCKET_ONCLOSE(event) {
      this.isConnected = false
      // 连接关闭时停掉心跳消息
      clearInterval(this.heartBeatTimer)
      this.heartBeatTimer = 0
      console.log(event)
    },
    // 发生错误
    SOCKET_ONERROR(event) {
      console.error(event)
    },
    // 收到服务端发送的消息
    SOCKET_ONMESSAGE(message) {
      this.message = message
      const data = message.d
      switch (message.op) {
        case operations.invalid_payload:
          console.log(message)
          alert('发生错误: \n' + (data['msg'] || JSON.stringify(data) || '未知错误'))
          if ('code' in data) {
            switch (data.code) {
              case 401:
              case 403:
                window.location.href = '/login'
                break
            }
          }
          break
        case operations.new_message:
          // TODO
          // 首先是在对话列表里更新该对话的最新修改时间
          useChatStore().touchChat(data)
          // 然后是在消息列表里添加该消息
          useMessageStore().addMessage(data)
      }
    },
    // 自动重连
    SOCKET_RECONNECT(count) {
      if (count <= 3) {
        console.info('服务器可能似了，正在重连...', count)
      } else {
        document.innerHTML = '<img src="/assets/server-exploded.png" alt="喜报：服务器炸了" />'
      }
    },
    // 重连错误
    SOCKET_RECONNECT_ERROR() {
      this.reconnectError = true
    },
  }
})
