<template>
  <v-btn icon class="no-drag-area" variant="text" @click="chatListRail = !chatListRail">
    <v-icon size="small">
      {{ chatListRail ? 'mdi-menu' : 'mdi-menu-open' }}
    </v-icon>
  </v-btn>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useSettingStore } from '@/store/app'
const { chatListRail } = storeToRefs(useSettingStore())
</script>
