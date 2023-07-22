import {defineStore} from "pinia"
import {operations} from "@/config/socket"

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
      this.socket = event.currentTarget
      this.isConnected = true
      // 连接成功时启动定时发送心跳消息，避免被服务器断开连接
      this.heartBeatTimer = setInterval(() => {
        this.isConnected && this.socket.sendObj({
          op: operations.heartbeat,
          d: {},
          t: ''
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
      switch (message.op) {
        case operations.invalid_payload:
          alert('发生错误: \n' + (message.d.msg || message.d || '未知错误'))
          break
      }
    },
    // 自动重连
    SOCKET_RECONNECT(count) {
      console.info('消息系统重连中...', count)
    },
    // 重连错误
    SOCKET_RECONNECT_ERROR() {
      this.reconnectError = true
    },
  }
})
