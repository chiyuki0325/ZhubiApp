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
let user = userStore.getUser(message.sender_id)
if (!user) {
  user = await api.get(
    `/tg/user/${message.sender_id}/info`,
    useAuth()
  ).then(res => {
    if (res.status !== 200) {
      return null
    } else {
      userStore.addUser(res.data.user)
      return res.data.user
    }
  })
}
const isNoUser = !user


</script>

<template>
  <PureTextMessage :message="message" v-if="message.type === messageType.text"/>
</template>

<style scoped>

</style>
