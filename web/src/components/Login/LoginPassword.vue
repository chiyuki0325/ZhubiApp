<script setup>
import {ref} from 'vue'
import Cookies from 'js-cookie'
import {calculatePasswordHash} from "@/utils"
import {api} from "@/utils"

let password = ref(''), loading = false

function handleLogin() {
  const passwordHash = calculatePasswordHash(password.value)
  loading = true
  api.post('/user/login/password', {
    password_hash: passwordHash
  }).then(response => {
    loading = false
    if (response.data.code === 200) {
      Cookies.set('token', response.data.token)
      window.location.href = '/chat'
    } else {
      alert('密码错误！')
    }
  })
}
</script>

<template>
  <v-card-subtitle class="text-center mt-0">
    使用设置的密码以登录。
  </v-card-subtitle>
  <div class="mx-6 py-6">
    <v-img src="/assets/password.svg" contain class="mx-auto ma-8"></v-img>
    <v-text-field
      v-model="password"
      variant="outlined"
      density="comfortable"
      prepend-inner-icon="mdi-lock"
      type="password"
      label="密码"
    >
    </v-text-field>
  </div>
  <div class="d-flex flex-row-reverse mx-3 align-center">
    <v-btn variant="text" color="primary" @click="handleLogin" :loading="loading">
      登录
      <template v-slot:loader>
        <v-progress-circular indeterminate></v-progress-circular>
      </template>
    </v-btn>
  </div>
</template>

<style scoped>

</style>
