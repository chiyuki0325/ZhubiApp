<script setup>
import {computed} from 'vue'
import themes from '@/plugins/themes'
import {useTheme} from 'vuetify'
import {useThemeStore} from '@/store/app'

const theme = useTheme()
const themeStore = useThemeStore()

const themeList = computed(() => {
  const themeList = []
  for (const key in themes) {
    themeList.push()
  }
  return themeList
})

function themeName(themeId) {
  return themeId.replace(/([A-Z])/g, ' $1').trim()
}
</script>


<template>
  <div class="theme-switcher">
    <v-dialog
        width="auto"
    >
      <template v-slot:activator="{ props }">
        <v-btn icon class="no-drag-area" variant="text" v-bind="props">
          <v-icon size="small">
            {{ theme.current.value.dark ? 'mdi-weather-night' : 'mdi-weather-sunny' }}
          </v-icon>
        </v-btn>
      </template>

      <v-card
          outlined
          color="surface"
          class="py-4 align-self-center"
          rounded="xl"
          width="90vw"
          max-width="450"
      >
        <div class="d-flex justify-center">
          <v-icon color="secondary" size="large">
            mdi-theme-light-dark
          </v-icon>
        </div>
        <v-card-title class="text-center">切换主题</v-card-title>
        <div class="mx-6 ">
          <div>
            <v-radio-group
                column
                v-model="theme.global.name.value"
            >
              <v-radio
                  v-for="theme in themes"
                  :key="theme.name"
                  :label="themeName(theme.name)"
                  :value="theme.name"
                  :color="themes[theme.name].primary"
              />
            </v-radio-group>
          </div>
        </div>
      </v-card>
    </v-dialog>
  </div>
</template>
