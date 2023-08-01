<script setup>
import {mediaUrl} from "@/utils"
import {computed, toRefs} from "vue"
import {useRoute} from "vue-router"

const props = defineProps({
  chat: Object,
})

const {chat} = toRefs(props)

const route = useRoute()

const subtitle = computed(() => {
  if (chat.value.last_message) {
    if (chat.value.last_message_sender) {
      return chat.value.last_message_sender + ": " + chat.value.last_message
    } else {
      return chat.value.last_message
    }
  } else {
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
