import Vue from 'vue'
import Router from 'vue-router'
import ElementUI from 'element-ui'
import Index from "../components/Index"
import Login from "../components/Login";
import 'element-ui/lib/theme-chalk/index.css';



Vue.use(Router)
Vue.use(ElementUI)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/index',
      name: 'index',
      component: Index,
      redirect: '/index/myHome',
      // 路由嵌套
      children:[
          {path: '/index/myHome',component: () => import('../components/myHome.vue')},
          {path: '/index/elementManage',component: () => import('../components/elementManage.vue')},
          {path: '/index/caseManage',component: () => import('../components/caseManage.vue')},
          {path: '/index/menu3',component: () => import('../components/Main3.vue')}
      ]
  }
]
})
