<script setup>
import {useUserStore} from "@/store/chat"
import {api, useAuth} from "@/utils"
import {messageType} from "@/config/enums"

import PureTextMessage from "./PureTextMessage.vue"

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
})

const message = props.message

// 获取用户信息
const userStore = useUserStore()
await userStore.tryFetchUser(message.sender_id)
let user = userStore.getUser(message.sender_id)


</script>

<template>
  <PureTextMessage :message="message" v-if="message.type === messageType.text"/>
</template>

<style scoped>

</style>
