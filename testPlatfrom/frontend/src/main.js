// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from 'axios'
import * as echarts from 'echarts';
// 引入状态管理
import store from './vuex/store';

Vue.prototype.$echarts = echarts
Vue.prototype.$axios = axios
Vue.use(axios);
axios.defaults.baseURL = '/api'// 使每次请求都会带一个 /api 前缀

Vue.config.productionTip = false
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,  //使用store vuex状态管理
  template: '<App/>',
  components: { App },
  render: h => h(App),
})
