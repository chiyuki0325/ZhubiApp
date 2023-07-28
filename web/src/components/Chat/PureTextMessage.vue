<script setup>
const props = defineProps({
  message: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div class="message">
    {{ message.text }}
  </div>
</template>

<style scoped>

</style>
