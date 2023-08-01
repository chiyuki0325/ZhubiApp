<script setup>
import {mediaUrl} from "@/utils"
import {computed, toRefs} from "vue"
import {useRoute} from "vue-router"

import {useChatStore, useMessageStore} from "@/store/chat"

const props = defineProps({
  chat: Object,
})

const {chat} = toRefs(props)
const messageStore = useMessageStore(), chatStore = useChatStore()
const route = useRoute()

const subtitle = computed(() => {
  if (chat.value.last_message) {
    if (chat.value.last_message_sender) {
      return chat.value.last_message_sender + ": " + chat.value.last_message
    } else {
      return chat.value.last_message
    }
  } else {
    if (chat.value.last_message_db_id) {
      // IDE 会报 vue/no-async-in-computed-properties 错误
      // 不管就好，因为这个函数内不需要他的结果
      messageStore.tryFetchMessageByDbId(chat.value.last_message_db_id).then(() => {
        const message = messageStore.getMessageByDbId(chat.value.last_message_db_id)
        chatStore.touchChat({...message})
      })
    } else {
      return ''
    }
    return '[消息 No.' + chat.value.last_message_db_id + ']'
  }
})

</script>

<template>
  <v-list-item
    :prepend-avatar="mediaUrl(chat.photo_file_id)"
    :title="chat.title"
    :subtitle="subtitle"
    :active="route.params.id == chat.id"
    class="drawer-item rounded-pill"
    :to="`/chat/${chat.id}`"
  />
</template>

<style scoped>
</style>
