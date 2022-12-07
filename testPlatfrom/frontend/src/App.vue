<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>

import myHome from './components/myHome.vue'

export default {
  name: 'app',
  components: {
    myHome
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;

}
body{
  margin: 0;
  padding: 0;
}
</style>
