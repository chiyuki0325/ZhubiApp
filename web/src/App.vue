<template>
  <router-view />
</template>

<script setup>
  import {useThemeStore} from "@/store/app"
  import {useTheme} from "vuetify"
  useTheme().global.name.value = useThemeStore().theme
</script>
