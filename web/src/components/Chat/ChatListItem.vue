<script setup>
import {mediaUrl} from "@/utils"
import {toRefs} from "vue"
import {useRoute} from "vue-router"

const props = defineProps({
  chat: Object,
})

const {chat} = toRefs(props)

const route = useRoute()

</script>

<template>
  <v-list-item
    :prepend-avatar="mediaUrl(chat.photo_file_id)"
    :title="chat.title"
    :subtitle="chat.last_message_db_id"
    :active="route.params.id == chat.id"
    class="drawer-item rounded-pill"
    :to="`/chat/${chat.id}`"
  />
</template>

<style scoped>

</style>
