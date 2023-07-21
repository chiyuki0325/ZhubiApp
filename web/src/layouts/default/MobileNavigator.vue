<script setup>

import {computed, ref} from "vue"
import navigatorItems from "@/config/navigator"
import {storeToRefs} from "pinia"
import {useSettingStore} from "@/store/app"

const nav = computed(() => navigatorItems)
const {tab} = storeToRefs(useSettingStore())
function switchTab(selectedTab) {
  tab.value = selectedTab
}
// coding here
</script>
<template>
  <v-bottom-navigation
    color="surfaceVariant"
    class="app-bottom-nav"
    height="64"
    order="-2"
    :elevation="0"
    mode="shift"
  >
    <v-btn
      v-for="item in nav"
      :key="item.val"
      :value="item.val"
      color="secondaryContainer"
      @click="switchTab(item.val)"
      active-class=""
      :class="{
        'v-btn--selected': tab === item.val
      }"
      >
      <div class="bar-icon rounded-xl">
        <v-icon>{{ item.icon }}</v-icon>
      </div>

      <span class="bar-label">{{ item.title }}</span>
    </v-btn>
  </v-bottom-navigation>
</template>
<style scoped lang="scss">
.app-bottom-nav {
  :deep(.v-bottom-navigation__content) {
    justify-content: space-evenly;
    .v-btn {
      .v-btn__content {
        gap: 4px;
        .bar-icon {
          width: 64px;
          height: 32px;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: background-color 0.3s ease;
          i {
            transition: all 0.3s ease;
          }
        }
        .bar-label {
          color: rgb(var(--v-theme-onSurfaceVariant));
        }
      }
      &.v-btn--selected {
        .bar-icon {
          background-color: rgb(var(--v-theme-secondaryContainer));
          i {
            color: rgb(var(--v-theme-onSurface));
          }
        }
        .bar-label {
          color: rgb(var(--v-theme-onSurface));
        }
      }
    }
  }
}
/* scoped css */
</style>
