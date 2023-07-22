import {apiUrl} from "@/config/config"
import {useWebSocketStore} from "@/store/app"

const {
  getSequence,
  increaseSequence,
  getHeartBeatLostCount,
  increaseHeartBeatLostCount
} = useWebSocketStore()

let ws

export const operations = {
  heartbeat: 0,
  ping: 1,
  pong: 2,
  invalid_payload: 1000
}

export const operation = (operation, data = {}, sequence = getSequence()) => {
  const operationString = JSON.stringify(
    {
      op: operation,
      d: data,
      s: sequence,
    })
  increaseSequence()
  return operationString
}

// 心跳检测及自动重连代码改自：
// https://www.cnblogs.com/tugenhua0707/p/8648044.html
function reconnectFunc() {
  let lockReconnect = false  //避免重复连接
  let reconnectionTimeOut
  return function () {
    if (lockReconnect) {
      return
    }
    lockReconnect = true;
    //没连接上会一直重连，设置延迟避免请求过多
    reconnectionTimeOut && clearTimeout(reconnectionTimeOut)
    reconnectionTimeOut = setTimeout(function () {
      createWebSocket()
      lockReconnect = false
    }, 4000)
  }
}

const reconnect = reconnectFunc()

function heartBeatCheckFunc() {
  const timeout = 30000  // 30s
  let clientTimeOut, serverTimeOut
  return function () {
    clientTimeOut && clearTimeout(clientTimeOut)
    serverTimeOut && clearTimeout(serverTimeOut)
    clientTimeOut = setTimeout(() => {
      ws.send(operation(operations.heartbeat))
      serverTimeOut = setTimeout(() => {
        // 服务器超时，说明连接已经断开
        increaseHeartBeatLostCount()
        if (getHeartBeatLostCount() > 3) {
          // 断线了
          alert('与服务器的连接已经断开！')
        }
        reconnect()
      }, timeout)
    }, timeout)
  }
}

const heartBeatCheck = heartBeatCheckFunc()

export function createWebSocket() {
  ws = new WebSocket(apiUrl.replace('http', 'ws') + '/ws')
  ws.onopen = wsOnOpen
  ws.onmessage = wsOnMessage
}

function wsOnOpen() {
  // 开始心跳检测
  heartBeatCheck()
}

function wsOnMessage(payload) {
  heartBeatCheck()
  //switch (payload.op) {
  //}
}
