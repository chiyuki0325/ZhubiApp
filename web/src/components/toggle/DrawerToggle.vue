<template>
  <v-btn icon class="no-drag-area" variant="text" @click="rail = !rail">
    <v-icon size="small">
      {{ rail ? 'mdi-menu' : 'mdi-menu-open' }}
    </v-icon>
  </v-btn>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useSettingStore } from '@/store/app'
const { rail } = storeToRefs(useSettingStore())
</script>
