<template>
  <v-app>
    <mobile-navigator v-if="xs"/>
    <default-navigator v-if="smAndUp"/>
    <default-view/>
  </v-app>
</template>

<script setup>
import DefaultNavigator from './Navigator.vue'
import MobileNavigator from "./MobileNavigator.vue"
import DefaultView from './View.vue'
import {useDisplay} from "vuetify"

const display = useDisplay()
const {xs, smAndUp} = display
</script>
