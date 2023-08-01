<script setup>
import {computed} from 'vue'
import {storeToRefs} from 'pinia'
import {useSettingStore} from '@/store/app'
import navigatorItems from '@/config/navigator'

// 组件
import ThemeSwitcher from "@/components/ThemeSwitcher.vue"
import DrawerToggle from "@/components/toggle/DrawerToggle.vue"

const {rail, tab} = storeToRefs(useSettingStore())


const nav = computed(() => navigatorItems)

function switchTab(selectedTab) {
  tab.value = selectedTab
}
</script>

<template>
  <v-navigation-drawer
    :rail="rail"
    rail-width="72"
    border="none"
    disable-route-watcher
    permanent
  >
    <div class="px-3 pt-1 mt-1">
      <drawer-toggle/>
    </div>

    <div class="content-warp flex-fill no-drag-area no-select" :class="{ 'rail-nav': rail }">
      <v-list class="list-content d-flex flex-column justify-center" rounded :nav="true">
        <v-list-item
          v-for="item in nav"
          :key="item.val"
          class="drawer-item rounded-pill"
          active-class="text-primary"
          :style="{ minHeight: '56px' }"
          @click="switchTab(item.val)"
          :active="item.val === tab"
        >
          <template #prepend>
            <div class="d-flex justify-center align-center" :style="{ width: '40px', height: '40px' }">
              <v-icon size="small" :icon="item.icon" color="primary"></v-icon>
            </div>
          </template>
          <v-list-item-title class="font-weight-bold">
            {{ item.title }}
          </v-list-item-title>
        </v-list-item>
      </v-list>
    </div>


    <template v-slot:append>
      <div class="px-3 pt-1 mt-1">
        <theme-switcher/>
      </div>
      <div class="px-3 pt-1 mt-1"></div>
    </template>
  </v-navigation-drawer>
</template>

<style scoped>
.no-select {
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
}
</style>
