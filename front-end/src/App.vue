<template>
  <NavigationBar v-if="!hideNavigation"/>
  <router-view/>
  <ToastContainer/>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavigationBar from './components/common/NavigationBar.vue'
import ToastContainer from './components/common/ToastContainer.vue'

const route = useRoute()

// 네비게이션을 숨길 라우트들
const hideNavigation = computed(() => {
  return ['login', 'signup', 'reset-password'].includes(route.name)
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100vh;
  overflow: hidden;
}

body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  overflow: hidden;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
