<script setup>
import Message from "./Message.vue"
import {computed} from "vue"
import {useTheme} from "vuetify"

const message = {
  "id": 5935,
  "tg_id": 106254,
  "type": 0,
  "unsupported_type": 9,
  "sender_id": 1778185820,
  "sender_chat_id": null,
  "chat_id": -1001642840004,
  "send_at": "2023-07-28T20:24:05",
  "text": "Hello world",
  "caption": null,
  "mentioned": false,
  "title": null,
  "sticker": null,
  "photo_id": null,
  "photo_spoiler": false,
  "system_message_type": 9,
  "system_message": null,
  "outgoing": true,
  "reply_to_tg_id": null,
  "forward_from_user_name": null,
  "forward_from_chat_name": null,
  "via_bot_username": null,
  "deleted": false
}  // 仅为示例，实际上应该从 props 传入

const date = computed(() => (new Date(message.send_at)).toLocaleString())
const cardColor = computed(() => (
  message.deleted ? 'surface' : (message.outgoing ? 'primaryContainer' : 'onPrimary')
))

const theme = useTheme()
const colors = theme.current.value.colors
const textColor = computed(() => (
  message.deleted ? colors.gray : (message.outgoing ? colors.onPrimaryContainer : colors.onBackground)
))
</script>

<template>
  <div
    class="message-wrapper d-flex flex-row"
    :class="{
      'justify-end': message.outgoing,
      'justify-start': !message.outgoing,
    }"
  >
    <Suspense>
      <v-card
        min-width="150"
        max-width="400"
        :color="cardColor"
        :style="{
            color: textColor
        }"
        class="pa-2"
      >

        <Message
          :message="message"
          v-if="!message.deleted"
        />
        <div
          class="message-deleted"
          :class="{
            'text-grey': message.deleted,
        }"
          v-else
        >[已删除]
        </div>

        <div class="message-date text-right text-sm-caption">
          {{ date }}
        </div>
      </v-card>
    </Suspense>
  </div>
</template>

<style scoped>
</style>
