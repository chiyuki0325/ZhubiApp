<script setup>
import ChatListItem from "./ChatListItem.vue"
import {computed} from "vue"
import {storeToRefs} from "pinia"
import {useChatStore} from "@/store/chat"
import {useSettingStore} from "@/store/app"
import {api, useAuth, isShowChat} from "@/utils"
import {useRouter} from "vue-router"
import ChatListToggle from "@/components/toggle/ChatListToggle.vue"
import {useDisplay} from "vuetify"

const display = useDisplay()
const {xs} = display

const chatStore = useChatStore()
const {chats} = storeToRefs(chatStore)

const {tab, chatListRail} = storeToRefs(useSettingStore())

const router = useRouter()

// 获取聊天列表
let chatsToSet
try {
  chatsToSet = await api.get('/tg/chat/list', useAuth()).then(res => res.data.chats)
} catch (e) {
  if (e.response.status === 401) {
    console.error('获取聊天列表失败，可能是登录过期，请重新登录。')
    router.push('/login')
  }
}
chatStore.setChats(chatsToSet)
chatStore.sortByDate()

</script>

<template>
  <div class="chat-list content-warp no-drag-area no-select">
    <v-navigation-drawer
      permanent
      :rail="xs ? chatListRail : false"
      :width="xs ? '100vw' : 300"
    >
    <div class="px-3 pt-1 mt-1 chat-list-toggle" v-if="xs">
      <chat-list-toggle />
    </div>

      <!-- 置顶聊天 -->
      <v-list class="list-content d-flex flex-column justify-center" rounded :nav="true">
        <template
          v-for="chat in chats"
          :key="chat.id">
          <ChatListItem
            v-if="chat.pinned && isShowChat(chat.type, tab)"
            :chat="chat"
          />
        </template>
      </v-list>
      <!-- 非置顶聊天 -->
      <v-list class="list-content d-flex flex-column justify-center" rounded :nav="true">
        <template
          v-for="chat in chats"
          :key="chat.id">
          <ChatListItem
            v-if="!chat.pinned && isShowChat(chat.type, tab)"
            :chat="chat"
          />
        </template>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<style scoped>
.no-select {
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
}
</style>
