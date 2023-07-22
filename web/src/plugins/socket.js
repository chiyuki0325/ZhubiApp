import vueNativeWebSocket from 'vue-native-websocket-vue3'
import {useWebSocketStore} from "@/store/socket"
import {store} from "@/store"
import {apiUrl} from "@/config/config"

export default {
  install: (app) => {
    const webSocketUrl = apiUrl.replace('http', 'ws') + '/ws'
    const webSocketStore = useWebSocketStore(store)
    app.use(vueNativeWebSocket, webSocketUrl, {
      store: webSocketStore,
      format: 'json',
      connectManually: true,
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 3000,
    })
  }
}
