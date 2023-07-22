<script>
// 因为 vue-native-websocket-vue3 插件严重过时
// 还建立在已经被弃用的 vuex 之上，对 pinia 支持还是 pr 进来的
// 对新的 composition api 以及 pinia 状态管理组件支持缺失
// 所以只能以 options api 来写这个组件
export default {
  mounted() {
    this.$connect()
  }
}
</script>

<template>

</template>
