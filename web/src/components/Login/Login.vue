<script async setup>
import {api} from "@/utils"
import LoginPassword from "./LoginPassword.vue"


// 获取登录方式
const loginMethod = await api.get('/user/login/method').then(response => {
  return response.data.method
})

const showDialog = true
</script>

<template>
  <v-main>
    <div class="text-center">
      <v-dialog v-model="showDialog">
        <v-card
          outlined
          color="surface"
          class="py-4 align-self-center"
          rounded="xl"
          width="90vw"
          max-width="450"
        >
          <!--登录卡片内部-->
          <!--账号图标-->
          <div class="d-flex justify-center">
            <v-icon color="secondary" size="large">
              mdi-login-variant
            </v-icon>
          </div>
          <v-card-title class="text-center">登录 ZhubiApp</v-card-title>
          <LoginPassword v-if="loginMethod === 'password'"/>
        </v-card>
      </v-dialog>
    </div>
  </v-main>
</template>

<style scoped>

</style>
